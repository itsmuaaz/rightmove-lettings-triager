import unittest
import time
import threading
from unittest.mock import patch, MagicMock
from tfl_client import TflClient

class TestTflClientRateLimitingIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TflClient(min_interval=0.1) # Fast interval for test

    @patch('urllib.request.urlopen')
    def test_fetch_journey_waits_for_slot(self, mock_urlopen):
        """Test that _fetch_journey calls _wait_for_slot before making a request."""
        # Ensure cache miss
        self.client.cache_dir = ".tfl_cache_integration_test" # Use distinct cache dir
        import shutil
        import os
        if os.path.exists(self.client.cache_dir):
            shutil.rmtree(self.client.cache_dir)
            
        # Mock API
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b'{"journeys": [{"duration": 10}]}'
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        # Spy on _wait_for_slot
        with patch.object(self.client, '_wait_for_slot', wraps=self.client._wait_for_slot) as mock_wait:
            self.client._fetch_journey((51.5, 0.1), (51.6, 0.2), {}, 1)
            
            # Verify wait was called
            mock_wait.assert_called()
            
    @patch('urllib.request.urlopen')
    def test_fetch_journey_cached_skips_wait(self, mock_urlopen):
        """Test that a cache hit does NOT wait for a slot."""
        # Pre-populate cache
        key = self.client._get_cache_key((51.5, 0.1), (51.6, 0.2), {})
        self.client._save_cache(key, {'journeys': [{'duration': 5}]})
        
        # Spy on _wait_for_slot
        with patch.object(self.client, '_wait_for_slot', wraps=self.client._wait_for_slot) as mock_wait:
            self.client._fetch_journey((51.5, 0.1), (51.6, 0.2), {}, 1)
            
            # Verify wait was NOT called (because no API call made)
            mock_wait.assert_not_called()
            mock_urlopen.assert_not_called()

if __name__ == '__main__':
    unittest.main()
