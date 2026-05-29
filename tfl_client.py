"""Module for interacting with the TfL Unified API.

This module provides a client for fetching journey times (Public Transport and Cycling)
from the Transport for London API, with support for caching and rate limiting.
"""

import json
import urllib.request
import urllib.parse
import sys
import time
import hashlib
import os
import threading
from datetime import datetime
from typing import Optional, Tuple, Any, Dict
from benchmark_utils import get_next_benchmark_time

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

    def _load_cache(self, key: str, ignore_expiration: bool = False) -> Optional[Any]:
        """Loads data from cache if available."""
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                
                # Check for new structure with metadata
                if isinstance(data, dict) and "response" in data:
                    if not ignore_expiration:
                        # Check for expiration (arrival_benchmark in past)
                        benchmark_str = data.get("arrival_benchmark")
                        if benchmark_str:
                            try:
                                benchmark_time = datetime.fromisoformat(benchmark_str)
                                if datetime.now() > benchmark_time:
                                    sys.stderr.write(f"[CACHE BYPASS - STALE] TfL benchmark {benchmark_str} expired.\n")
                                    return None
                            except ValueError:
                                return None
                    return data["response"]
                else:
                    # Legacy file or unexpected format, delete and return None
                    try:
                        os.remove(cache_path)
                    except OSError:
                        pass
                    return None
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def _save_cache(self, key: str, data: Any) -> None:
        """Saves data to cache."""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        try:
            wrapped_data = {
                "calculated_at": datetime.now().isoformat(),
                "arrival_benchmark": get_next_benchmark_time().isoformat(),
                "response": data
            }
            with open(cache_path, 'w') as f:
                json.dump(wrapped_data, f)
        except IOError as e:
            sys.stderr.write(f"Failed to write to cache: {e}\n")

    def _extract_journey_data(self, data: dict) -> Optional[Dict[str, Any]]:
        """Extracts duration and fare data from the API response."""
        journeys = data.get('journeys', [])
        if not journeys:
            return None
            
        # Find the shortest journey
        best_journey = min(journeys, key=lambda j: j.get('duration', 999))
        duration = best_journey.get('duration')
        
        # Extract fares
        fares = {}
        fare_data = best_journey.get('fare')
        if fare_data:
            total_cost = fare_data.get('totalCost')
            if total_cost:
                fares['total_cost'] = total_cost
            
            breakdown = fare_data.get('fares', [])
            total_peak = 0
            total_off_peak = 0
            has_breakdown = False
            
            for item in breakdown:
                has_breakdown = True
                cost = item.get('cost', 0)
                # Use peak/offPeak if available and non-zero
                peak = item.get('peak')
                if not peak and cost > 0:
                    peak = cost
                
                off_peak = item.get('offPeak')
                if not off_peak and cost > 0:
                    off_peak = cost
                
                total_peak += peak
                total_off_peak += off_peak
            
            if has_breakdown:
                fares['peak'] = total_peak
                fares['off_peak'] = total_off_peak

        return {
            'duration': duration,
            'fares': fares
        }

    def _fetch_journey(self, from_coords: Tuple[float, float], to_coords: Tuple[float, float], params: dict, max_retries: int, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Internal helper to fetch journey data with specific parameters."""
        # Check cache first
        cache_key = self._get_cache_key(from_coords, to_coords, params)
        mode = "Cycling" if params.get('mode') == 'cycle' else "Public Transport"
        if not force_refresh:
            cached_data = self._load_cache(cache_key)
            if cached_data:
                sys.stderr.write(f"[CACHE HIT] TfL commute ({mode}) {from_coords} to {to_coords}\n")
                return self._extract_journey_data(cached_data)
            else:
                cache_path = os.path.join(self.cache_dir, f"{cache_key}.json")
                if not os.path.exists(cache_path):
                    sys.stderr.write(f"[CACHE MISS] TfL commute ({mode}) {from_coords} to {to_coords} not found.\n")

        sys.stderr.write(f"[CACHE FETCH] Fetching TfL commute ({mode}) {from_coords} to {to_coords} from API...\n")
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
                    if response.status == 429:
                        sys.stderr.write(f"TfL API Rate Limit (429). Backing off for 20s...\n")
                        time.sleep(20)
                        continue
                        
                    if response.status != 200:
                        sys.stderr.write(f"TfL API Error: Status {response.status}\n")
                        fallback_data = self._load_cache(cache_key, ignore_expiration=True)
                        if fallback_data:
                            sys.stderr.write(f"[API ERROR] [FAIL] TfL fetch ({mode}) failed - Falling back to stale cached commute data.\n")
                            return self._extract_journey_data(fallback_data)
                        sys.stderr.write(f"[API ERROR] [FAIL] TfL fetch ({mode}) for {from_coords} to {to_coords}\n")
                        return None
                    data = json.loads(response.read().decode('utf-8'))
                    
                    # Save to cache
                    self._save_cache(cache_key, data)
                    sys.stderr.write(f"[API SUCCESS] [PASS] TfL fetch ({mode}) for {from_coords} to {to_coords}\n")
                    return self._extract_journey_data(data)
            except Exception as e:
                sys.stderr.write(f"TfL API Attempt {attempt + 1} failed: {str(e)}\n")
                sys.stderr.write(f"URL: {url}\n")
                if attempt < max_retries - 1:
                    time.sleep(1) # Simple backoff
                else:
                    fallback_data = self._load_cache(cache_key, ignore_expiration=True)
                    if fallback_data:
                        sys.stderr.write(f"[API ERROR] [FAIL] TfL fetch ({mode}) failed - Falling back to stale cached commute data.\n")
                        return self._extract_journey_data(fallback_data)
                    sys.stderr.write(f"[API ERROR] [FAIL] TfL fetch ({mode}) for {from_coords} to {to_coords}\n")
                    return None
        fallback_data = self._load_cache(cache_key, ignore_expiration=True)
        if fallback_data:
            sys.stderr.write(f"[API ERROR] [FAIL] TfL fetch ({mode}) failed - Falling back to stale cached commute data.\n")
            return self._extract_journey_data(fallback_data)
        sys.stderr.write(f"[API ERROR] [FAIL] TfL fetch ({mode}) for {from_coords} to {to_coords}\n")
        return None

    def get_journey_data(self, from_coords: Tuple[float, float], to_coords: Tuple[float, float], max_retries: int = 3, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Fetches public transport journey data (duration, fares) between two coordinates.

        Args:
            from_coords: Tuple of (lat, lon) for the origin.
            to_coords: Tuple of (lat, lon) for the destination.
            max_retries: Number of retry attempts on failure.
            force_refresh: Whether to bypass the cache.

        Returns:
            Dictionary with 'duration' (mins) and 'fares' (dict), or None if failed.
        """
        benchmark = get_next_benchmark_time()
        params = {
            "date": benchmark.strftime("%Y%m%d"),
            "time": benchmark.strftime("%H%M"),
            "timeIs": "Arriving"
        }
        return self._fetch_journey(from_coords, to_coords, params, max_retries, force_refresh=force_refresh)

    def get_commute_time(self, from_coords: Tuple[float, float], to_coords: Tuple[float, float], max_retries: int = 3, force_refresh: bool = False) -> Optional[int]:
        """Fetches public transport commute time in minutes between two coordinates with retries.

        Args:
            from_coords: Tuple of (lat, lon) for the origin.
            to_coords: Tuple of (lat, lon) for the destination.
            max_retries: Number of retry attempts on failure.
            force_refresh: Whether to bypass the cache.

        Returns:
            Shortest journey duration in minutes, or None if failed.
        """
        result = self.get_journey_data(from_coords, to_coords, max_retries, force_refresh)
        if result:
            return result.get('duration')
        return None

    def get_cycling_time(self, from_coords: Tuple[float, float], to_coords: Tuple[float, float], max_retries: int = 3, force_refresh: bool = False) -> Optional[int]:
        """Fetches cycling commute time in minutes between two coordinates with retries.

        Args:
            from_coords: Tuple of (lat, lon) for the origin.
            to_coords: Tuple of (lat, lon) for the destination.
            max_retries: Number of retry attempts on failure.
            force_refresh: Whether to bypass the cache.

        Returns:
            Shortest cycling duration in minutes, or None if failed.
        """
        params = {
            'mode': 'cycle',
            # 'cyclePreference': 'allTheWay',
            # 'bikeProficiency': 'moderate'
        }
        result = self._fetch_journey(from_coords, to_coords, params, max_retries, force_refresh=force_refresh)
        if result:
            return result.get('duration')
        return None

def cleanup_stale_caches(cache_dir: str) -> None:
    """Scans the given directory and deletes stale TfL cache JSON files."""
    if not os.path.exists(cache_dir):
        return
        
    now = datetime.now()
    try:
        files = os.listdir(cache_dir)
    except OSError:
        return
        
    for filename in files:
        if filename.endswith(".json"):
            file_path = os.path.join(cache_dir, filename)
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                
                # Check arrival_benchmark
                if isinstance(data, dict):
                    benchmark_str = data.get("arrival_benchmark")
                    if benchmark_str:
                        benchmark_time = datetime.fromisoformat(benchmark_str)
                        if now > benchmark_time:
                            # Stale! Delete it
                            try:
                                os.remove(file_path)
                            except OSError:
                                pass
                    else:
                        # Legacy file without arrival_benchmark, delete it to be clean
                        try:
                            os.remove(file_path)
                        except OSError:
                            pass
            except (json.JSONDecodeError, IOError, ValueError):
                # Malformed file or read error, delete it
                try:
                    os.remove(file_path)
                except OSError:
                    pass
