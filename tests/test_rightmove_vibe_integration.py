import unittest
from unittest.mock import patch, MagicMock
from rightmove_search import process_property
from vibe_client import VibeClient

class TestRightmoveVibeIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_property = {
            'id': '123',
            'address': '123 High Street, SW14 7AB',
            'latitude': 51.5,
            'longitude': -0.1,
            '_original': {}
        }

    @patch('rightmove_search.calculator')
    @patch('rightmove_search.amenity_calculator')
    @patch('rightmove_search.note_manager')
    @patch('rightmove_search.history_manager')
    @patch('rightmove_search.vibe_client')
    @patch('rightmove_search.search_state')
    def test_process_property_injects_vibe(self, mock_state, mock_vibe, mock_history, mock_note, mock_amenity, mock_calc):
        # Mock dependencies
        mock_calc.calculate.return_value = {'commute_time': 30, 'distance': 5}
        mock_amenity.calculate.return_value = {}
        mock_vibe.get_vibes.return_value = {
            "SW14": {
                "score": 8,
                "summary": "Nice"
            }
        }
        
        # Call function
        result = process_property(self.mock_property, 0, 1)
        
        # Verify vibe data is injected
        self.assertIn('vibe', result)
        self.assertEqual(result['vibe']['score'], 8)
        self.assertEqual(result['vibe']['summary'], "Nice")
        
        # Verify get_vibes was called with correct district
        mock_vibe.get_vibes.assert_called_once()
        args = mock_vibe.get_vibes.call_args[0][0]
        self.assertIn("SW14", args)

if __name__ == '__main__':
    unittest.main()
