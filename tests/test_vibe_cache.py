import unittest
import os
import json
import shutil
import threading
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from vibe_client import VibeClient

class TestVibeCache(unittest.TestCase):
    def setUp(self):
        self.test_cache_file = ".vibe_cache_test_unique.json"
        if os.path.exists(self.test_cache_file):
            os.remove(self.test_cache_file)
            
        self.client = VibeClient(cache_file=self.test_cache_file)

    def tearDown(self):
        if os.path.exists(self.test_cache_file):
            os.remove(self.test_cache_file)

    def test_load_cache_fresh_vibe(self):
        """Test that a fresh vibe cache entry (within TTL) is loaded successfully."""
        # Setup fresh cache entry
        fresh_time = (datetime.now() - timedelta(days=5)).isoformat()
        vibe_data = {
            "SW14": {
                "score": 8,
                "summary": "Leafy green village",
                "cached_at": fresh_time
            }
        }
        with open(self.test_cache_file, 'w') as f:
            json.dump(vibe_data, f)
            
        # Reload client cache
        self.client.cache = self.client._load_cache()
        
        # Query vibes
        result = self.client.get_vibes(["SW14"])
        self.assertEqual(result.get("SW14", {}).get("score"), 8)

    @patch("vibe_client.VibeClient._fetch_from_gemini")
    def test_load_cache_expired_vibe(self, mock_fetch):
        """Test that an expired vibe cache entry (older than TTL) is bypassed and re-fetched."""
        # Setup expired cache entry
        expired_time = (datetime.now() - timedelta(days=self.client.ttl_days + 1)).isoformat()
        vibe_data = {
            "SW14": {
                "score": 8,
                "summary": "Leafy green village",
                "cached_at": expired_time
            }
        }
        with open(self.test_cache_file, 'w') as f:
            json.dump(vibe_data, f)
            
        # Reload client cache
        self.client.cache = self.client._load_cache()
        
        # Mock Gemini fetch to return new data
        mock_fetch.return_value = {
            "SW14": {
                "score": 9,
                "summary": "Updated summary"
            }
        }
        
        # Query vibes - must trigger re-fetch and return score 9
        result = self.client.get_vibes(["SW14"])
        self.assertEqual(result.get("SW14", {}).get("score"), 9)

    @patch("vibe_client.VibeClient._fetch_from_gemini")
    def test_load_cache_legacy_vibe(self, mock_fetch):
        """Test that a legacy cache entry (missing cached_at timestamp) is treated as expired/stale."""
        # Setup legacy cache entry (no cached_at field)
        vibe_data = {
            "SW14": {
                "score": 8,
                "summary": "Leafy green village"
            }
        }
        with open(self.test_cache_file, 'w') as f:
            json.dump(vibe_data, f)
            
        # Reload client cache
        self.client.cache = self.client._load_cache()
        
        # Mock Gemini fetch
        mock_fetch.return_value = {
            "SW14": {
                "score": 9,
                "summary": "Updated summary"
            }
        }
        
        # Query vibes - must trigger re-fetch and return score 9
        result = self.client.get_vibes(["SW14"])
        self.assertEqual(result.get("SW14", {}).get("score"), 9)

    @patch("vibe_client.VibeClient._fetch_from_gemini")
    def test_save_vibe_injects_timestamp(self, mock_fetch):
        """Test that saving fetched vibes correctly injects the 'cached_at' ISO timestamp."""
        # Mock Gemini fetch
        mock_fetch.return_value = {
            "SW14": {
                "score": 8,
                "summary": "Nice area"
            }
        }
        
        # Fetch SW14 (triggers fetch and save)
        self.client.get_vibes(["SW14"])
        
        # Verify cached_at exists in disk file and is close to now
        with open(self.test_cache_file, 'r') as f:
            data = json.load(f)
            
        cached_entry = data.get("SW14", {})
        self.assertIn("cached_at", cached_entry)
        
        cached_time = datetime.fromisoformat(cached_entry["cached_at"])
        self.assertTrue(datetime.now() - cached_time < timedelta(seconds=10))

    def test_concurrent_vibe_caching(self):
        """Test that concurrent vibe requests do not cause write collisions or cache overrides."""
        # Mock Gemini fetch to return unique score with latency
        def mock_fetch(locations):
            time.sleep(0.05) # Introduce latency to trigger race conditions
            loc = locations[0]
            return {
                loc: {
                    "score": int(loc[-1]),
                    "summary": f"Vibe for {loc}"
                }
            }
            
        with patch("vibe_client.VibeClient._fetch_from_gemini", side_effect=mock_fetch):
            threads = []
            for i in range(1, 6):
                loc_name = f"LOC{i}"
                t = threading.Thread(target=self.client.get_vibes, args=([loc_name],))
                threads.append(t)
                
            for t in threads:
                t.start()
                
            for t in threads:
                t.join()
                
        # Reload the disk file and verify ALL 5 entries are saved correctly!
        with open(self.test_cache_file, 'r') as f:
            disk_data = json.load(f)
            
        self.assertEqual(len(disk_data), 5)
        for i in range(1, 6):
            self.assertIn(f"LOC{i}", disk_data)
            self.assertEqual(disk_data[f"LOC{i}"]["score"], i)

if __name__ == '__main__':
    unittest.main()