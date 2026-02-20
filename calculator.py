from utils import haversine

class CommuteCalculator:
    def __init__(self, tfl_client=None, destination=None):
        self.tfl_client = tfl_client
        self.destination = destination

    def calculate(self, property_data):
        """Calculate commute time and distance for a property."""
        location = property_data.get('location', {})
        lat, lon = location.get('latitude'), location.get('longitude')
        
        if not lat or not lon:
            return {'commute_time': None, 'distance': float('inf')}
            
        distance = haversine(lat, lon, self.destination[0], self.destination[1])
        commute_time = None
        
        if self.tfl_client:
            commute_time = self.tfl_client.get_commute_time((lat, lon), self.destination)
            
        return {
            'commute_time': commute_time,
            'distance': distance
        }
