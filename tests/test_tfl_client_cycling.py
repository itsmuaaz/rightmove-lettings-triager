import unittest
from unittest.mock import patch, MagicMock
from tfl_client import TflClient

class TestTflClientCycling(unittest.TestCase):
    def setUp(self):
        self.client = TflClient(app_id="test_id", app_key="test_key")

    @patch("urllib.request.urlopen")
    def test_get_cycling_time_success(self, mock_urlopen):
        # Mock API response
        mock_response = MagicMock()
        mock_response.status = 200
        # Cycling journey usually returns duration
        mock_response.read.return_value = b'{"journeys": [{"duration": 25}]}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Call the client
        duration = self.client.get_cycling_time((51.5007, -0.1246), (51.5349, -0.1238))
        
        self.assertEqual(duration, 25)
        
        # Check URL parameters
        args, kwargs = mock_urlopen.call_args
        req = args[0]
        self.assertIn("mode=cycle", req.full_url)
        self.assertIn("cyclePreference=allTheWay", req.full_url)
        self.assertIn("bikeProficiency=moderate", req.full_url)
        self.assertIn("app_id=test_id", req.full_url)

    @patch("urllib.request.urlopen")
    def test_get_cycling_time_error(self, mock_urlopen):
        # Mock API 404
        mock_response = MagicMock()
        mock_response.status = 404
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        duration = self.client.get_cycling_time((51.5, -0.1), (51.6, -0.2))
        self.assertIsNone(duration)

    @patch("urllib.request.urlopen")
    def test_get_cycling_time_no_journeys(self, mock_urlopen):
        # Mock API response with no journeys
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"journeys": []}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        duration = self.client.get_cycling_time((51.5, -0.1), (51.6, -0.2))
        self.assertIsNone(duration)

if __name__ == "__main__":
    unittest.main()
