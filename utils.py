"""Utility module for geographical calculations."""
from __future__ import annotations

import math
import re
import urllib.parse
import urllib.request
import json
import sys
from datetime import datetime

_GEOCODE_CACHE = {}

# Constants for Work Location
WORK_ADDRESS = "6 Pancras Square, N1C 4AG"
WORK_COORDS = (51.5349, -0.1238)

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates the distance in miles between two coordinates.

    Args:
        lat1: Latitude of the first point.
        lon1: Longitude of the first point.
        lat2: Latitude of the second point.
        lon2: Longitude of the second point.

    Returns:
        The distance between the two points in miles.
    """
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 0.621371  # km to miles

def format_date(iso_date: str) -> str:
    """Formats an ISO date string into a human-readable 'ago' format.

    Args:
        iso_date: ISO 8601 date string (e.g., '2023-10-27T10:00:00Z').

    Returns:
        Human-readable string (e.g., '2 days ago', 'Today', 'Unknown').
    """
    if not iso_date:
        return 'Unknown'
    
    try:
        # Handle simplified ISO format often used by APIs
        dt = datetime.strptime(iso_date.split('T')[0], '%Y-%m-%d')
        now = datetime.now()
        diff = now - dt
        
        if diff.days == 0:
            return 'Today'
        elif diff.days == 1:
            return 'Yesterday'
        else:
            return f"{diff.days} days ago"
    except ValueError:
        return 'Unknown'

def generate_google_maps_url(origin_address: str) -> str:
    """Generates a Google Maps directions URL.

    Args:
        origin_address: The starting address string.

    Returns:
        A Google Maps URL for public transport directions to work.
    """
    params = {
        "api": "1",
        "origin": origin_address,
        "destination": WORK_ADDRESS,
        "travelmode": "transit"
    }
    query = urllib.parse.urlencode(params)
    return f"https://www.google.com/maps/dir/?{query}"

def generate_tfl_url(origin_address: str, origin_coords: tuple[float, float] = None) -> str:
    """Generates a TfL Journey Planner URL.

    Args:
        origin_address: The starting address string.
        origin_coords: Optional tuple of (latitude, longitude) for the origin.

    Returns:
        A TfL Journey Planner URL to work.
    """
    params = {
        "InputFrom": origin_address,
        "InputTo": WORK_ADDRESS,
        "ToId": f"{WORK_COORDS[0]},{WORK_COORDS[1]}"
    }
    if origin_coords:
        params["FromId"] = f"{origin_coords[0]},{origin_coords[1]}"
        
    query = urllib.parse.urlencode(params)
    return f"https://tfl.gov.uk/plan-a-journey/results?{query}"

def extract_postcode_district(address: str) -> str | None:
    """Extracts the postcode district (e.g., 'SW14', 'E1') from an address string.

    Args:
        address: The address string.

    Returns:
        The postcode district string, or None if not found.
    """
    if not address:
        return None
    
    # Regex for UK postcode districts (Outward Code)
    # Matches: SW14 7AB -> SW14, E1 8AB -> E1, N1C 4AG -> N1C
    match = re.search(r'\b([A-Z]{1,2}\d[A-Z\d]?)\b', address.upper())
    if match:
        return match.group(1)
    return None

def reverse_geocode(lat: float, lon: float) -> str | None:
    """Reverse-geocodes latitude and longitude to a postcode district using postcodes.io.

    Args:
        lat: Latitude float.
        lon: Longitude float.

    Returns:
        The postcode district (outcode) if found, otherwise None.
    """
    coords = (lat, lon)
    if coords in _GEOCODE_CACHE:
        return _GEOCODE_CACHE[coords]

    url = f"https://api.postcodes.io/postcodes?lon={lon}&lat={lat}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        with urllib.request.urlopen(req, timeout=3) as response:
            status = getattr(response, "status", 200)
            if status == 200:
                res_data = json.loads(response.read().decode('utf-8'))
                result_list = res_data.get('result')
                if result_list and isinstance(result_list, list) and len(result_list) > 0:
                    outcode = result_list[0].get('outcode')
                    if outcode:
                        _GEOCODE_CACHE[coords] = outcode
                        return outcode
    except Exception as e:
        sys.stderr.write(f"Geocoding Error for coords {coords}: {e}\n")
        
    _GEOCODE_CACHE[coords] = None
    return None

def extract_location_for_vibe(address: str, coords: tuple[float, float] = None) -> str | None:
    """Extracts a location key for vibe lookup (postcode district or full address).

    Args:
        address: The address string.
        coords: Optional Tuple of (lat, lon) coordinates to reverse-geocode if address has no postcode.

    Returns:
        The postcode district if found, otherwise the fallback geocoded postcode, the full address, or None.
    """
    district = extract_postcode_district(address)
    if district:
        return district
    
    if coords and isinstance(coords, tuple) and len(coords) == 2:
        lat, lon = coords
        if lat is not None and lon is not None:
            fallback_district = reverse_geocode(lat, lon)
            if fallback_district:
                return fallback_district
    
    if address and address.strip():
        # Clean address slightly (remove extra whitespace)
        return address.strip()
    
    return None

def create_sort_key(property_data: dict, sort_by: str = 'smart_score', mode: str = 'min') -> float | str:
    """Generates a sort key for a property based on the specified criteria.

    Args:
        property_data: The dictionary containing property details.
        sort_by: The field to sort by ('price', 'smart_score', 'vibe_score', 'commute', 'added_on').
        mode: The commute mode ('min', 'transport', 'cycling'). Only used if sort_by='commute'.

    Returns:
        A comparable value (float or string).
    """
    if sort_by == 'price':
        val = property_data.get('price')
        if isinstance(val, (int, float)):
            return val
        
        parsed = extract_numeric_price(str(val)) if val else None
        return parsed if parsed is not None else float('inf')

    elif sort_by == 'smart_score':
        val = property_data.get('smart_score')
        if val == "N/A" or val is None:
            return -1.0
        try:
            return float(val)
        except (ValueError, TypeError):
            return -1.0

    elif sort_by == 'vibe_score':
        # Vibe is usually a dict in raw data: {'score': 5, ...}
        # In enriched data it might be flat, but we sort raw data.
        vibe = property_data.get('vibe')
        if isinstance(vibe, dict):
             val = vibe.get('score')
        else:
             val = property_data.get('vibe_score') # Fallback if already enriched or flat
             
        if val == "N/A" or val is None:
            return -1.0
        try:
            return float(val)
        except (ValueError, TypeError):
            return -1.0

    elif sort_by == 'added_on':
        val = property_data.get('added_on')
        return val if val else ''

    elif sort_by == 'commute':
        commute = property_data.get('commute_time')
        cycling = property_data.get('commute_cycling')
        
        c_val = commute if commute is not None else float('inf')
        cy_val = cycling if cycling is not None else float('inf')

        if mode == 'transport':
            return c_val
        elif mode == 'cycling':
            return cy_val
        else:
            return min(c_val, cy_val)
            
    return 0

def get_sort_key(p):
    """Determine the sort key for a property based on shortest commute."""
    commute = p.get('commute_time')
    cycling = p.get('commute_cycling')
    
    if commute is None and cycling is None:
        return float('inf')
    
    if commute is None:
        return cycling
    
    if cycling is None:
        return commute
        
    return min(commute, cycling)

def extract_numeric_price(price_str: str) -> float | None:
    """Extracts the numeric value from a price string (e.g., '£2,000 pcm').
    
    Args:
        price_str: The raw price string.
        
    Returns:
        The extracted numeric value as a float, or None if invalid.
    """
    if not price_str or "POA" in price_str.upper() or "CONTACT" in price_str.upper():
        return None
        
    # Remove everything except digits and decimal points
    cleaned = re.sub(r'[^\d.]', '', price_str)
    
    if not cleaned:
        return None
        
    try:
        return float(cleaned)
    except ValueError:
        return None

def get_days_since(iso_date: str) -> int | None:
    """Calculates the number of days between an ISO date and today.

    Args:
        iso_date: ISO 8601 date string (e.g., '2023-10-27T10:00:00Z').

    Returns:
        The number of days (int) or None if the date is invalid.
    """
    if not iso_date:
        return None
    
    try:
        # Handle simplified ISO format often used by APIs
        # Extract just the date part (YYYY-MM-DD)
        date_part = iso_date.split('T')[0]
        dt = datetime.strptime(date_part, '%Y-%m-%d')
        now = datetime.now()
        
        # We compare dates only (ignoring time)
        diff = now.date() - dt.date()
        return diff.days
    except ValueError:
        return None
