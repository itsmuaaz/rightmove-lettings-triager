import json
import urllib.request
import urllib.parse

class TflClient:
    def __init__(self, app_id=None, app_key=None):
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = "https://api.tfl.gov.uk/Journey/JourneyResults"

    def get_commute_time(self, from_coords, to_coords):
        """Fetch commute time in minutes between two coordinates."""
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

        try:
            with urllib.request.urlopen(url) as response:
                if response.status != 200:
                    return None
                data = json.loads(response.read().decode('utf-8'))
                journeys = data.get('journeys', [])
                if not journeys:
                    return None
                # Return the shortest duration found
                return min(j.get('duration', 999) for j in journeys)
        except Exception:
            return None
