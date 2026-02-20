import unittest
from unittest.mock import MagicMock, patch
from calculator import CommuteCalculator

class TestCommuteCalculator(unittest.TestCase):
    def setUp(self):
        self.mock_tfl_client = MagicMock()
        self.destination = (51.5349, -0.1238) # Work
        self.calculator = CommuteCalculator(tfl_client=self.mock_tfl_client, destination=self.destination)

    def test_calculate_commute_success(self):
        # Mock TflClient success
        self.mock_tfl_client.get_commute_time.return_value = 25
        self.mock_tfl_client.get_cycling_time.return_value = 15
        
        prop = {'location': {'latitude': 51.5007, 'longitude': -0.1246}}
        result = self.calculator.calculate(prop)
        
        self.assertEqual(result['commute_time'], 25)
        self.assertEqual(result['commute_cycling'], 15)
        self.assertAlmostEqual(result['distance'], 2.36, places=2)

    def test_calculate_commute_fallback(self):
        # Mock TflClient failure (None)
        self.mock_tfl_client.get_commute_time.return_value = None
        
        prop = {'location': {'latitude': 51.5007, 'longitude': -0.1246}}
        result = self.calculator.calculate(prop)
        
        self.assertIsNone(result['commute_time'])
        self.assertAlmostEqual(result['distance'], 2.36, places=2)

    def test_calculate_commute_no_location(self):
        prop = {}
        result = self.calculator.calculate(prop)
        self.assertIsNone(result['commute_time'])
        self.assertEqual(result['distance'], float('inf'))

    def test_calculate_no_destination(self):
        self.calculator.destination = None
        prop = {'location': {'latitude': 51.5007, 'longitude': -0.1246}}
        result = self.calculator.calculate(prop)
        self.assertIsNone(result['commute_time'])
        self.assertEqual(result['distance'], float('inf'))

if __name__ == "__main__":
    unittest.main()
