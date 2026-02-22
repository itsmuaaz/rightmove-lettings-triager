import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from tfl_client import TflClient

class TestTflClient(unittest.TestCase):
    def setUp(self):
        self.test_cache_dir = ".tfl_cache_test_old"
        self.client = TflClient(app_id="test_id", app_key="test_key")
        self.client.cache_dir = self.test_cache_dir
        
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)
        os.makedirs(self.test_cache_dir)

    def tearDown(self):
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)

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
        # Check if correct Request was called
        args, kwargs = mock_urlopen.call_args
        req = args[0]
        self.assertIn("app_id=test_id", req.full_url)
        self.assertIn("app_key=test_key", req.full_url)
        self.assertIn("51.5007,-0.1246", req.full_url)
        self.assertIn("51.5349,-0.1238", req.full_url)
        self.assertEqual(req.get_header("User-agent"), "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

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
