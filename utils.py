"""Utility module for geographical calculations."""

import math
from datetime import datetime

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
