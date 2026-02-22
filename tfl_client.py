"""Module for interacting with the TfL Unified API."""

import json
import urllib.request
import urllib.parse
import sys
import time
import hashlib
import os
import threading
from typing import Optional, Tuple, Any

class TflClient:
    """Client for fetching journey results from Transport for London."""

    def __init__(self, app_id: Optional[str] = None, app_key: Optional[str] = None, min_interval: float = 1.5):
        """Initializes the TfL client.

        Args:
            app_id: The TfL App ID (optional for low limits).
            app_key: The TfL App Key (optional for low limits).
            min_interval: Minimum time in seconds between API requests.
        """
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = "https://api.tfl.gov.uk/Journey/JourneyResults"
        self.cache_dir = ".tfl_cache"
        self.min_interval = min_interval
        self.last_request_time = 0.0
        self.lock = threading.Lock()

    def _wait_for_slot(self) -> None:
        """Blocks until the rate limit interval has passed."""
        with self.lock:
            current_time = time.time()
            elapsed = current_time - self.last_request_time
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_request_time = time.time()

    def _get_cache_key(self, from_coords: Tuple[float, float], to_coords: Tuple[float, float], params: dict) -> str:
        """Generates a unique cache key based on request parameters."""
        key_str = f"{from_coords}-{to_coords}-{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_str.encode('utf-8')).hexdigest()

    def _load_cache(self, key: str) -> Optional[Any]:
        """Loads data from cache if available."""
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def _save_cache(self, key: str, data: Any) -> None:
        """Saves data to cache."""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            sys.stderr.write(f"Failed to write to cache: {e}\n")

    def _fetch_journey(self, from_coords: Tuple[float, float], to_coords: Tuple[float, float], params: dict, max_retries: int) -> Optional[int]:
        """Internal helper to fetch journey time with specific parameters."""
        # Check cache first
        cache_key = self._get_cache_key(from_coords, to_coords, params)
        cached_data = self._load_cache(cache_key)
        if cached_data:
            journeys = cached_data.get('journeys', [])
            if not journeys:
                return None
            return min(j.get('duration', 999) for j in journeys)

        from_str = f"{from_coords[0]},{from_coords[1]}"
        to_str = f"{to_coords[0]},{to_coords[1]}"
        
        url = f"{self.base_url}/{from_str}/to/{to_str}"
        
        # Add auth params to a copy to avoid side effects
        request_params = params.copy()
        if self.app_id:
            request_params['app_id'] = self.app_id
        if self.app_key:
            request_params['app_key'] = self.app_key
            
        if request_params:
            url += "?" + urllib.parse.urlencode(request_params)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        for attempt in range(max_retries):
            try:
                # Rate limit before request
                self._wait_for_slot()
                
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    if response.status != 200:
                        sys.stderr.write(f"TfL API Error: Status {response.status}\n")
                        return None
                    data = json.loads(response.read().decode('utf-8'))
                    
                    # Save to cache
                    self._save_cache(cache_key, data)
                    
                    journeys = data.get('journeys', [])
                    if not journeys:
                        return None
                    # Return the shortest duration found
                    return min(j.get('duration', 999) for j in journeys)
            except Exception as e:
                sys.stderr.write(f"TfL API Attempt {attempt + 1} failed: {str(e)}\n")
                if attempt < max_retries - 1:
                    time.sleep(1) # Simple backoff
                else:
                    return None
        return None

    def get_commute_time(self, from_coords: Tuple[float, float], to_coords: Tuple[float, float], max_retries: int = 3) -> Optional[int]:
        """Fetches public transport commute time in minutes between two coordinates with retries.

        Args:
            from_coords: Tuple of (lat, lon) for the origin.
            to_coords: Tuple of (lat, lon) for the destination.
            max_retries: Number of retry attempts on failure.

        Returns:
            Shortest journey duration in minutes, or None if failed.
        """
        return self._fetch_journey(from_coords, to_coords, {}, max_retries)

    def get_cycling_time(self, from_coords: Tuple[float, float], to_coords: Tuple[float, float], max_retries: int = 3) -> Optional[int]:
        """Fetches cycling commute time in minutes between two coordinates with retries.

        Args:
            from_coords: Tuple of (lat, lon) for the origin.
            to_coords: Tuple of (lat, lon) for the destination.
            max_retries: Number of retry attempts on failure.

        Returns:
            Shortest cycling duration in minutes, or None if failed.
        """
        params = {
            'mode': 'cycle',
            'cyclePreference': 'allTheWay',
            'bikeProficiency': 'moderate'
        }
        return self._fetch_journey(from_coords, to_coords, params, max_retries)
