import urllib.request
import urllib.parse
import urllib.error
import json
import os
import hashlib
import time
from utils import haversine

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

class AmenityClient:
    """Client for fetching amenities from Overpass API with caching and retries."""

    def __init__(self, cache_dir=".amenity_cache"):
        self.cache_dir = cache_dir
        if self.cache_dir and not os.path.exists(self.cache_dir):
            try:
                os.makedirs(self.cache_dir)
            except Exception:
                # Fallback to no caching if dir cannot be created
                self.cache_dir = None
                
        self.categories = {
            "supermarket": ['node["shop"="supermarket"]', 'way["shop"="supermarket"]'],
            "gym": ['node["leisure"="fitness_centre"]', 'way["leisure"="fitness_centre"]'],
            "park": ['way["leisure"="park"]', 'relation["leisure"="park"]'],
            "hospital": ['node["amenity"="hospital"]', 'way["amenity"="hospital"]'],
            "doctors": ['node["amenity"="doctors"]']
        }

    def _get_cache_key(self, lat: float, lon: float, radius: int, category: str) -> str:
        """Generates a cache key based on query parameters."""
        key = f"{round(lat, 4)}:{round(lon, 4)}:{radius}:{category}"
        return hashlib.md5(key.encode('utf-8')).hexdigest()

    def fetch_amenities(self, lat: float, lon: float, radius: int, category: str, max_attempts: int = 3) -> list:
        """Fetches amenities of a specific category within a radius, using cache and retries."""
        if category not in self.categories:
            return []
            
        cache_key = self._get_cache_key(lat, lon, radius, category)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json") if self.cache_dir else None
        
        if cache_file and os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
            
        filters = self.categories[category]
        query_parts = []
        for f in filters:
            query_parts.append(f'{f}(around:{radius},{lat},{lon});')
            
        query = f'[out:json][timeout:25];({"".join(query_parts)});out center;'
        
        for attempt in range(max_attempts):
            try:
                data = urllib.parse.urlencode({'data': query}).encode('utf-8')
                req = urllib.request.Request(OVERPASS_URL, data=data)
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    elements = result.get('elements', [])
                    
                    amenities = []
                    for el in elements:
                        el_lat = el.get('lat') or el.get('center', {}).get('lat')
                        el_lon = el.get('lon') or el.get('center', {}).get('lon')
                        
                        if el_lat is None or el_lon is None:
                            continue
                            
                        dist_miles = haversine(lat, lon, el_lat, el_lon)
                        dist_meters = dist_miles * 1609.34
                        
                        amenities.append({
                            'name': el.get('tags', {}).get('name', 'Unknown'),
                            'distance': round(dist_meters, 0),
                            'lat': el_lat,
                            'lon': el_lon
                        })
                    
                    amenities.sort(key=lambda x: x['distance'])
                    
                    if cache_file:
                        try:
                            with open(cache_file, 'w') as f:
                                json.dump(amenities, f)
                        except Exception:
                            pass
                            
                    return amenities
                    
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionError):
                if attempt < max_attempts - 1:
                    time.sleep(1.5 * (attempt + 1))
                continue
            except Exception:
                # Other exceptions (like JSON parsing error) might not be transient
                break
                
        return []
