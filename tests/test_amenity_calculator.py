import unittest
from unittest.mock import MagicMock
from amenity_calculator import AmenityCalculator

class TestAmenityCalculator(unittest.TestCase):
    def test_calculate_amenities(self):
        """Test calculation of nearest amenities across categories."""
        mock_client = MagicMock()
        
        # Mock results for different categories
        mock_client.fetch_all_amenities.return_value = {
            "supermarket": [{"name": "Tesco", "distance": 200}],
            "gym": [{"name": "PureGym", "distance": 500}],
            "park": [{"name": "Green Park", "distance": 100}],
            "hospital": [{"name": "Hospital", "distance": 1500}],
            "doctors": [{"name": "Local GP", "distance": 800}]
        }
        
        calc = AmenityCalculator(amenity_client=mock_client, radius=1000)
        results = calc.calculate(51.5, -0.1)
        
        self.assertEqual(results['supermarket']['name'], "Tesco")
        self.assertEqual(results['gym']['name'], "PureGym")
        self.assertEqual(results['park']['name'], "Green Park")
        # Healthcare should pick the nearest (800 < 1500)
        self.assertEqual(results['healthcare']['name'], "Local GP")
        
        # Verify bulk fetch was called once
        self.assertEqual(mock_client.fetch_all_amenities.call_count, 1)

    def test_calculate_amenities_missing(self):
        """Test handling when some categories have no results."""
        mock_client = MagicMock()
        mock_client.fetch_all_amenities.return_value = {
            "supermarket": [],
            "gym": [],
            "park": [],
            "hospital": [],
            "doctors": []
        }
        
        calc = AmenityCalculator(amenity_client=mock_client)
        results = calc.calculate(51.5, -0.1)
        
        self.assertIsNone(results['supermarket'])
        self.assertIsNone(results['gym'])

if __name__ == '__main__':
    unittest.main()
