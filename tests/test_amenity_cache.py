import unittest
import os
import shutil
import json
from amenity_client import AmenityClient
from unittest.mock import patch, MagicMock

class TestAmenityCache(unittest.TestCase):
    def setUp(self):
        self.cache_dir = ".test_amenity_cache"
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
            
    def tearDown(self):
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)

    def test_caching_mechanism(self):
        """Test that bulk API results are cached and reused."""
        lat, lon, radius = 51.5, -0.1, 1000
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps({
                "elements": [{"lat": 51.501, "lon": -0.101, "tags": {"shop": "supermarket", "name": "Cache Test"}}]
            }).encode('utf-8')
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response
            
            client = AmenityClient(cache_dir=self.cache_dir)
            
            # First call - should trigger API
            result1 = client.fetch_all_amenities(lat, lon, radius)
            self.assertEqual(len(result1['supermarket']), 1)
            self.assertEqual(mock_urlopen.call_count, 1)
            
            # Second call - should use cache
            result2 = client.fetch_all_amenities(lat, lon, radius)
            self.assertEqual(len(result2['supermarket']), 1)
            self.assertEqual(mock_urlopen.call_count, 1) # Still 1
            
            self.assertEqual(result1, result2)

if __name__ == '__main__':
    unittest.main()
