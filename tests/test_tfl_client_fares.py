import unittest
from unittest.mock import patch, MagicMock
from tfl_client import TflClient

class TestTflClientFares(unittest.TestCase):
    def setUp(self):
        self.client = TflClient(app_id="test", app_key="test")
        self.client._wait_for_slot = MagicMock()

    @patch("urllib.request.urlopen")
    def test_get_journey_data_returns_fares(self, mock_urlopen):
        # Mock API response with fare data
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b"""
        {
            "journeys": [
                {
                    "duration": 45,
                    "fare": {
                        "totalCost": 350,
                        "fares": [
                            {
                                "peak": 350,
                                "offPeak": 280
                            }
                        ]
                    }
                }
            ]
        }
        """
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Call the client (method doesn't exist yet, should fail)
        result = self.client.get_journey_data((51.5, -0.1), (51.6, -0.2))
        
        self.assertIsNotNone(result)
        self.assertEqual(result['duration'], 45)
        self.assertIn('fares', result)
        self.assertEqual(result['fares']['peak'], 350)
        self.assertEqual(result['fares']['off_peak'], 280)

if __name__ == "__main__":
    unittest.main()
