"""Module for interacting with the TfL Unified API."""

import json
import urllib.request
import urllib.parse
import sys
import time
from typing import Optional, Tuple, Any

class TflClient:
    """Client for fetching journey results from Transport for London."""

    def __init__(self, app_id: Optional[str] = None, app_key: Optional[str] = None):
        """Initializes the TfL client.

        Args:
            app_id: The TfL App ID (optional for low limits).
            app_key: The TfL App Key (optional for low limits).
        """
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = "https://api.tfl.gov.uk/Journey/JourneyResults"

    def _fetch_journey(self, from_coords: Tuple[float, float], to_coords: Tuple[float, float], params: dict, max_retries: int) -> Optional[int]:
        """Internal helper to fetch journey time with specific parameters."""
        from_str = f"{from_coords[0]},{from_coords[1]}"
        to_str = f"{to_coords[0]},{to_coords[1]}"
        
        url = f"{self.base_url}/{from_str}/to/{to_str}"
        
        # Add auth params
        if self.app_id:
            params['app_id'] = self.app_id
        if self.app_key:
            params['app_key'] = self.app_key
            
        if params:
            url += "?" + urllib.parse.urlencode(params)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        for attempt in range(max_retries):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    if response.status != 200:
                        sys.stderr.write(f"TfL API Error: Status {response.status}\n")
                        return None
                    data = json.loads(response.read().decode('utf-8'))
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
