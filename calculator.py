"""Module for calculating property-related commute metrics."""

from typing import Dict, Optional, Tuple, Any
from utils import haversine

class CommuteCalculator:
    """Calculates commute time and distance from a property to a destination."""

    def __init__(self, tfl_client: Any = None, destination: Optional[Tuple[float, float]] = None):
        """Initializes the calculator.

        Args:
            tfl_client: An instance of TflClient to fetch commute times.
            destination: A tuple of (latitude, longitude) for the destination.
        """
        self.tfl_client = tfl_client
        self.destination = destination

    def calculate(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates commute time and distance for a property.

        Args:
            property_data: A dictionary containing property details from Rightmove.

        Returns:
            A dictionary with 'commute_time' (mins) and 'distance' (miles).
        """
        location = property_data.get('location', {})
        lat, lon = location.get('latitude'), location.get('longitude')
        
        if not lat or not lon or not self.destination:
            return {'commute_time': None, 'distance': float('inf')}
            
        distance = haversine(lat, lon, self.destination[0], self.destination[1])
        commute_time = None
        
        if self.tfl_client:
            commute_time = self.tfl_client.get_commute_time((lat, lon), self.destination)
            
        return {
            'commute_time': commute_time,
            'distance': distance
        }
