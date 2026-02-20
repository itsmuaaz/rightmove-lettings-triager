from typing import Dict, Any, Optional

class AmenityCalculator:
    """Calculates proximity to various amenities for a property."""

    def __init__(self, amenity_client=None, radius: int = 1000):
        """Initializes the calculator.

        Args:
            amenity_client: An instance of AmenityClient to fetch data.
            radius: Search radius in meters.
        """
        self.amenity_client = amenity_client
        self.radius = radius

    def calculate(self, lat: float, lon: float) -> Dict[str, Any]:
        """Calculates nearest instance of each amenity category.

        Args:
            lat: Latitude of the property.
            lon: Longitude of the property.

        Returns:
            A dictionary containing the nearest amenity for each category.
        """
        default_res = {
            'supermarket': None,
            'gym': None,
            'park': None,
            'healthcare': None
        }
        
        if not self.amenity_client or not lat or not lon:
            return default_res
            
        all_amenities = self.amenity_client.fetch_all_amenities(lat, lon, self.radius)
        
        results = {}
        
        # Supermarket
        supermarkets = all_amenities.get('supermarket', [])
        results['supermarket'] = supermarkets[0] if supermarkets else None
        
        # Gym
        gyms = all_amenities.get('gym', [])
        results['gym'] = gyms[0] if gyms else None
        
        # Park
        parks = all_amenities.get('park', [])
        results['park'] = parks[0] if parks else None
        
        # Healthcare (combine hospital and doctors)
        hospitals = all_amenities.get('hospital', [])
        doctors = all_amenities.get('doctors', [])
        healthcare = hospitals + doctors
        # Sort combined list by distance
        healthcare.sort(key=lambda x: x['distance'])
        results['healthcare'] = healthcare[0] if healthcare else None
        
        return results
