import json
import urllib.request
import urllib.parse
import sys
import time

class TflClient:
    def __init__(self, app_id=None, app_key=None):
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = "https://api.tfl.gov.uk/Journey/JourneyResults"

    def get_commute_time(self, from_coords, to_coords, max_retries=3):
        """Fetch commute time in minutes between two coordinates with retries."""
        from_str = f"{from_coords[0]},{from_coords[1]}"
        to_str = f"{to_coords[0]},{to_coords[1]}"
        
        url = f"{self.base_url}/{from_str}/to/{to_str}"
        params = {}
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
