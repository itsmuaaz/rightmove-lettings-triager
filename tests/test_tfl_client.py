import unittest
from unittest.mock import patch, MagicMock
from tfl_client import TflClient

class TestTflClient(unittest.TestCase):
    def setUp(self):
        self.client = TflClient(app_id="test_id", app_key="test_key")

    @patch("urllib.request.urlopen")
    def test_get_commute_time_success(self, mock_urlopen):
        # Mock API response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"journeys": [{"duration": 35}]}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Call the client
        duration = self.client.get_commute_time((51.5007, -0.1246), (51.5349, -0.1238))
        
        self.assertEqual(duration, 35)
        # Check if correct URL was called
        args, kwargs = mock_urlopen.call_args
        url = args[0]
        self.assertIn("app_id=test_id", url)
        self.assertIn("app_key=test_key", url)
        self.assertIn("51.5007,-0.1246", url)
        self.assertIn("51.5349,-0.1238", url)

    @patch("urllib.request.urlopen")
    def test_get_commute_time_no_journeys(self, mock_urlopen):
        # Mock API response with no journeys
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"journeys": []}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        duration = self.client.get_commute_time((51.5, -0.1), (51.6, -0.2))
        self.assertIsNone(duration)

    @patch("urllib.request.urlopen")
    def test_get_commute_time_error_status(self, mock_urlopen):
        # Mock API response with 404
        mock_response = MagicMock()
        mock_response.status = 404
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        duration = self.client.get_commute_time((51.5, -0.1), (51.6, -0.2))
        self.assertIsNone(duration)

    @patch("urllib.request.urlopen")
    @patch("time.sleep")
    def test_get_commute_time_exception(self, mock_sleep, mock_urlopen):
        # Mock urlopen throwing an exception
        mock_urlopen.side_effect = Exception("API Down")

        duration = self.client.get_commute_time((51.5, -0.1), (51.6, -0.2))
        self.assertIsNone(duration)
        self.assertEqual(mock_urlopen.call_count, 3) # Should retry 3 times

    @patch("urllib.request.urlopen")
    @patch("time.sleep")
    def test_get_commute_time_retry_success(self, mock_sleep, mock_urlopen):
        # Fail once, then succeed
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"journeys": [{"duration": 40}]}'
        mock_response.__enter__.return_value = mock_response
        
        mock_urlopen.side_effect = [Exception("Temporary error"), mock_response]

        duration = self.client.get_commute_time((51.5, -0.1), (51.6, -0.2))
        self.assertEqual(duration, 40)
        self.assertEqual(mock_urlopen.call_count, 2)
        mock_sleep.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
