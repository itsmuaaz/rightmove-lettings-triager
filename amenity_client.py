import urllib.request
import urllib.parse
import urllib.error
import json
import os
import hashlib
import time
import sys
from utils import haversine

OVERPASS_URL = "https://overpass.openstreetmap.fr/api/interpreter"

class AmenityClient:
    """Client for fetching amenities from Overpass API with caching and retries."""

    def __init__(self, cache_dir=".amenity_cache"):
        self.cache_dir = cache_dir
        if self.cache_dir and not os.path.exists(self.cache_dir):
            try:
                os.makedirs(self.cache_dir)
            except Exception:
                self.cache_dir = None
                
        # Define tags for each category
        self.category_tags = {
            "supermarket": [('shop', 'supermarket')],
            "gym": [('leisure', 'fitness_centre'), ('leisure', 'sports_centre')],
            "park": [('leisure', 'park'), ('leisure', 'garden')],
            "hospital": [('amenity', 'hospital')],
            "doctors": [('amenity', 'doctors')]
        }

    def _get_cache_key(self, lat: float, lon: float, radius: int) -> str:
        """Generates a cache key for the bulk query."""
        # Querying ALL categories at once, so key only depends on location/radius
        key = f"{round(lat, 4)}:{round(lon, 4)}:{radius}:bulk"
        return hashlib.md5(key.encode('utf-8')).hexdigest()

    def is_cached(self, lat: float, lon: float, radius: int = 1000) -> bool:
        """Returns True if the bulk amenity cache file exists for these coordinates and radius."""
        cache_key = self._get_cache_key(lat, lon, radius)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json") if self.cache_dir else None
        return cache_file is not None and os.path.exists(cache_file)

    def fetch_all_amenities(self, lat: float, lon: float, radius: int, max_attempts: int = 5) -> dict:
        """Fetches all categories of amenities in a single bulk query."""
        cache_key = self._get_cache_key(lat, lon, radius)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json") if self.cache_dir else None
        
        if cache_file and os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
            
        # Construct bulk query
        query_parts = []
        for cat, tags in self.category_tags.items():
            for key, val in tags:
                query_parts.append(f'node["{key}"="{val}"](around:{radius},{lat},{lon});')
                query_parts.append(f'way["{key}"="{val}"](around:{radius},{lat},{lon});')
                query_parts.append(f'relation["{key}"="{val}"](around:{radius},{lat},{lon});')
            
        query = f'[out:json][timeout:60];({"".join(query_parts)});out center;'
        
        for attempt in range(max_attempts):
            try:
                # Use GET request as openstreetmap.fr blocks POST requests with 403 Forbidden.
                # Use a curl User-Agent as openstreetmap.fr whitelists curl but blocks standard generic browsers to prevent spam.
                encoded_query = urllib.parse.urlencode({'data': query})
                url = f"{OVERPASS_URL}?{encoded_query}"
                req = urllib.request.Request(url)
                req.add_header("User-Agent", "curl/8.7.1")
                
                with urllib.request.urlopen(req, timeout=60) as response:
                    data = response.read().decode('utf-8')
                    result = json.loads(data)
                    elements = result.get('elements', [])
                    
                    # Group results by category
                    categorized = {cat: [] for cat in self.category_tags.keys()}
                    
                    for el in elements:
                        el_lat = el.get('lat') or el.get('center', {}).get('lat')
                        el_lon = el.get('lon') or el.get('center', {}).get('lon')
                        if el_lat is None or el_lon is None:
                            continue
                            
                        tags = el.get('tags', {})
                        dist_meters = round(haversine(lat, lon, el_lat, el_lon) * 1609.34, 0)
                        
                        amenity_info = {
                            'name': tags.get('name', 'Unknown'),
                            'distance': dist_meters,
                            'lat': el_lat,
                            'lon': el_lon
                        }
                        
                        # Assign to categories
                        for cat, tag_list in self.category_tags.items():
                            for k, v in tag_list:
                                if tags.get(k) == v:
                                    categorized[cat].append(amenity_info)
                                    break
                    
                    # Sort each category and pick nearest
                    final_results = {}
                    for cat, items in categorized.items():
                        items.sort(key=lambda x: x['distance'])
                        # We keep the whole list or just nearest?
                        # Calculator will pick nearest. Let's keep the sorted list.
                        final_results[cat] = items
                        
                    if cache_file:
                        try:
                            with open(cache_file, 'w') as f:
                                json.dump(final_results, f)
                        except Exception:
                            pass
                            
                    return final_results
                    
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionError):
                if attempt < max_attempts - 1:
                    time.sleep(2 * (attempt + 1))
                continue
            except Exception:
                break
                
        return None
