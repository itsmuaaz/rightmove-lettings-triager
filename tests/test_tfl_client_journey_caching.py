import unittest
import os
import shutil
import json
from unittest.mock import patch, MagicMock
from tfl_client import TflClient

class TestTflClientJourneyCaching(unittest.TestCase):
    def setUp(self):
        self.test_cache_dir = ".tfl_cache_test_journey"
        self.client = TflClient()
        self.client.cache_dir = self.test_cache_dir
        
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)
        os.makedirs(self.test_cache_dir)

    def tearDown(self):
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)

    @patch('urllib.request.urlopen')
    def test_fetch_journey_cache_miss_saves_data(self, mock_urlopen):
        """Test that a cache miss calls the API and saves the result."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            'journeys': [{'duration': 25}]
        }).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        from_coords = (51.5, 0.1)
        to_coords = (51.6, 0.2)
        params = {'mode': 'tube'}

        # Execute
        duration = self.client._fetch_journey(from_coords, to_coords, params, max_retries=1)

        # Verify
        self.assertEqual(duration, 25)
        mock_urlopen.assert_called_once()
        
        # Verify cache file exists
        key = self.client._get_cache_key(from_coords, to_coords, params)
        cache_path = os.path.join(self.test_cache_dir, f"{key}.json")
        self.assertTrue(os.path.exists(cache_path))
        
        # Verify cache content
        with open(cache_path, 'r') as f:
            data = json.load(f)
            # data is now wrapped in metadata
            self.assertIn('response', data)
            self.assertEqual(data['response']['journeys'][0]['duration'], 25)

    @patch('urllib.request.urlopen')
    def test_fetch_journey_cache_hit_avoids_api(self, mock_urlopen):
        """Test that a cache hit returns data without calling the API."""
        from_coords = (51.5, 0.1)
        to_coords = (51.6, 0.2)
        params = {'mode': 'tube'}
        
        # Pre-populate cache
        key = self.client._get_cache_key(from_coords, to_coords, params)
        data = {'journeys': [{'duration': 15}]}
        self.client._save_cache(key, data)
        
        # Execute
        duration = self.client._fetch_journey(from_coords, to_coords, params, max_retries=1)
        
        # Verify
        self.assertEqual(duration, 15)
        mock_urlopen.assert_not_called()

if __name__ == '__main__':
    unittest.main()
