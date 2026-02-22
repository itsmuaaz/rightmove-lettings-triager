import unittest
import os
import shutil
import json
from unittest.mock import patch, MagicMock
from tfl_client import TflClient

class TestTflClientRepeatCalls(unittest.TestCase):
    def setUp(self):
        self.test_cache_dir = ".tfl_cache_test_repeat"
        self.client = TflClient()
        self.client.cache_dir = self.test_cache_dir
        
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)
        os.makedirs(self.test_cache_dir)

    def tearDown(self):
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)

    @patch('urllib.request.urlopen')
    def test_repeat_calls_use_cache(self, mock_urlopen):
        """Test that calling get_commute_time twice results in only one API call."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            'journeys': [{'duration': 30}]
        }).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        from_coords = (51.5074, 0.1278)
        to_coords = (51.5014, 0.1419)

        # First call
        duration1 = self.client.get_commute_time(from_coords, to_coords)
        self.assertEqual(duration1, 30)
        
        # Verify API called once
        self.assertEqual(mock_urlopen.call_count, 1)

        # Second call
        duration2 = self.client.get_commute_time(from_coords, to_coords)
        self.assertEqual(duration2, 30)

        # Verify API STILL called only once (cache hit)
        self.assertEqual(mock_urlopen.call_count, 1)

if __name__ == '__main__':
    unittest.main()
