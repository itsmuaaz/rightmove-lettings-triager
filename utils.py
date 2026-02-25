"""Utility module for geographical calculations."""

import math
import urllib.parse
from datetime import datetime

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
