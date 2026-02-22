import unittest
import os
import shutil
import json
import hashlib
from tfl_client import TflClient

class TestTflClientCaching(unittest.TestCase):
    def setUp(self):
        self.test_cache_dir = ".tfl_cache_test"
        self.client = TflClient()
        # Monkey patch the cache directory for testing
        self.client.cache_dir = self.test_cache_dir
        
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)
        os.makedirs(self.test_cache_dir)

    def tearDown(self):
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)

    def test_get_cache_key_consistency(self):
        """Test that the cache key is consistent for the same inputs."""
        from_coords = (51.5074, 0.1278)
        to_coords = (51.5014, 0.1419)
        params = {'mode': 'tube'}
        
        key1 = self.client._get_cache_key(from_coords, to_coords, params)
        key2 = self.client._get_cache_key(from_coords, to_coords, params)
        
        self.assertEqual(key1, key2)
        self.assertTrue(isinstance(key1, str))
        self.assertTrue(len(key1) > 0)

    def test_get_cache_key_uniqueness(self):
        """Test that different inputs produce different keys."""
        from_coords1 = (51.5074, 0.1278)
        to_coords1 = (51.5014, 0.1419)
        params1 = {'mode': 'tube'}
        
        from_coords2 = (51.5075, 0.1279) # Different start
        
        key1 = self.client._get_cache_key(from_coords1, to_coords1, params1)
        key2 = self.client._get_cache_key(from_coords2, to_coords1, params1)
        
        self.assertNotEqual(key1, key2)

    def test_save_and_load_cache(self):
        """Test saving data to cache and loading it back."""
        from_coords = (51.5074, 0.1278)
        to_coords = (51.5014, 0.1419)
        params = {'mode': 'tube'}
        data = {'journeys': [{'duration': 15}]}
        
        key = self.client._get_cache_key(from_coords, to_coords, params)
        
        # Save to cache
        self.client._save_cache(key, data)
        
        # Verify file exists
        expected_file = os.path.join(self.test_cache_dir, f"{key}.json")
        self.assertTrue(os.path.exists(expected_file))
        
        # Load from cache
        loaded_data = self.client._load_cache(key)
        self.assertEqual(loaded_data, data)

    def test_load_cache_miss(self):
        """Test loading a non-existent cache key."""
        key = "non_existent_key"
        loaded_data = self.client._load_cache(key)
        self.assertIsNone(loaded_data)

if __name__ == '__main__':
    unittest.main()
