import unittest
import time
import os
import shutil
from unittest.mock import patch, MagicMock
from tfl_client import TflClient

class TestTflClientBackoff(unittest.TestCase):
    def setUp(self):
        self.test_dir = ".tfl_cache_backoff_test"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        
        self.client = TflClient(min_interval=0.1)
        self.client.cache_dir = self.test_dir

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('time.sleep')
    @patch('urllib.request.urlopen')
    def test_backoff_on_429(self, mock_urlopen, mock_sleep):
        """Test that 429 response triggers aggressive backoff."""
        # Setup mock to fail with 429 then succeed
        mock_response_429 = MagicMock()
        mock_response_429.status = 429
        mock_response_429.__enter__.return_value = mock_response_429
        
        mock_response_200 = MagicMock()
        mock_response_200.status = 200
        mock_response_200.read.return_value = b'{"journeys": [{"duration": 15}]}'
        mock_response_200.__enter__.return_value = mock_response_200
        
        # urlopen returns 429 first, then 200
        mock_urlopen.side_effect = [mock_response_429, mock_response_200]

        duration = self.client._fetch_journey((51.5, 0.1), (51.6, 0.2), {}, 3)
        
        # Verify result
        self.assertEqual(duration, 15)
        
        # Verify backoff was called with 20s
        mock_sleep.assert_any_call(20)

    @patch('time.sleep')
    @patch('urllib.request.urlopen')
    def test_backoff_gives_up(self, mock_urlopen, mock_sleep):
        """Test that it eventually gives up after max retries."""
        mock_response_429 = MagicMock()
        mock_response_429.status = 429
        mock_response_429.__enter__.return_value = mock_response_429
        
        mock_urlopen.return_value = mock_response_429
        
        duration = self.client._fetch_journey((51.5, 0.1), (51.6, 0.2), {}, 2)
        
        self.assertIsNone(duration)
        self.assertEqual(mock_urlopen.call_count, 2)
        
        # Check that we backed off for 20s twice
        backoff_calls = [args[0] for args, _ in mock_sleep.call_args_list if args[0] == 20]
        self.assertEqual(len(backoff_calls), 2)

if __name__ == '__main__':
    unittest.main()
