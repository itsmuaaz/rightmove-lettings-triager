import unittest
import shutil
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
from tfl_client import TflClient
from datetime import datetime

class TestTflClientCache(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.client = TflClient()
        self.client.cache_dir = self.test_dir

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_save_cache_structure(self):
        # Test that _save_cache wraps the data with metadata
        key = "test_key"
        data = {"journeys": [{"duration": 30}]}
        
        with patch('tfl_client.datetime') as mock_datetime:
            mock_now = datetime(2023, 1, 1, 12, 0, 0)
            mock_datetime.now.return_value = mock_now
            # We mock isoformat explicitly if needed, but datetime objects have it
            
            self.client._save_cache(key, data)
            
            cache_path = os.path.join(self.test_dir, f"{key}.json")
            with open(cache_path, 'r') as f:
                saved_content = json.load(f)
            
            self.assertIn("calculated_at", saved_content)
            self.assertIn("response", saved_content)
            self.assertEqual(saved_content["response"], data)
            self.assertEqual(saved_content["calculated_at"], mock_now.isoformat())

    def test_load_cache_valid_wrapper(self):
        # Test loading a valid wrapped cache file
        key = "test_key_valid"
        data = {"journeys": [{"duration": 45}]}
        wrapped_content = {
            "calculated_at": "2023-01-01T12:00:00",
            "response": data
        }
        
        cache_path = os.path.join(self.test_dir, f"{key}.json")
        with open(cache_path, 'w') as f:
            json.dump(wrapped_content, f)
            
        loaded_data = self.client._load_cache(key)
        self.assertEqual(loaded_data, data)

    def test_load_cache_legacy_format(self):
        # Test loading a legacy cache file (raw response without wrapper)
        key = "test_key_legacy"
        data = {"journeys": [{"duration": 60}]}
        
        # Save raw data (simulating old format)
        cache_path = os.path.join(self.test_dir, f"{key}.json")
        with open(cache_path, 'w') as f:
            json.dump(data, f)
            
        # Should return None (cache miss) because it lacks the wrapper
        loaded_data = self.client._load_cache(key)
        self.assertIsNone(loaded_data)
        
        # Verify the file is deleted (optional, but good practice for cleanup)
        # The spec says "Existing legacy files... will be reset (deleted) upon implementation"
        # Ideally _load_cache should identify it's invalid and maybe delete it?
        # The plan says "Ensure legacy files are ignored or deleted"
        self.assertFalse(os.path.exists(cache_path))

if __name__ == '__main__':
    unittest.main()
