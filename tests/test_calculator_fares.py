import unittest
from unittest.mock import MagicMock
from calculator import CommuteCalculator

class TestCommuteCalculatorFares(unittest.TestCase):
    def setUp(self):
        self.mock_tfl_client = MagicMock()
        self.destination = (51.5349, -0.1238) # Work
        self.calculator = CommuteCalculator(tfl_client=self.mock_tfl_client, destination=self.destination)

    def test_calculate_propagates_fares(self):
        # Mock TflClient returning journey data (new method)
        self.mock_tfl_client.get_journey_data.return_value = {
            'duration': 45,
            'fares': {'peak': 350, 'off_peak': 280}
        }
        # Cycling time remains int (or could be dict, but calculator handles int currently)
        self.mock_tfl_client.get_cycling_time.return_value = 25
        
        prop = {'location': {'latitude': 51.5007, 'longitude': -0.1246}}
        result = self.calculator.calculate(prop)
        
        self.assertEqual(result['commute_time'], 45)
        self.assertIn('commute_fares', result)
        self.assertEqual(result['commute_fares']['peak'], 350)
        self.assertEqual(result['commute_fares']['off_peak'], 280)

if __name__ == "__main__":
    unittest.main()
