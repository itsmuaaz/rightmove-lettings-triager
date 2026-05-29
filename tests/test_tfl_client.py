import unittest
import os
import json
import shutil
from datetime import datetime
from unittest.mock import patch, MagicMock
from tfl_client import TflClient

class TestTflClient(unittest.TestCase):
    def setUp(self):
        self.test_cache_dir = ".tfl_cache_test_old"
        self.client = TflClient(app_id="test_id", app_key="test_key", min_interval=0.1)
        self.client.cache_dir = self.test_cache_dir
        
        # Disable rate limiting for these tests to focus on retry logic
        self.client._wait_for_slot = MagicMock()
        
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)
        os.makedirs(self.test_cache_dir)

    def tearDown(self):
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)

    @patch("tfl_client.get_next_benchmark_time")
    @patch("urllib.request.urlopen")
    def test_get_commute_time_success(self, mock_urlopen, mock_benchmark_time):
        # Mock benchmark time
        mock_benchmark_time.return_value = datetime(2026, 3, 3, 9, 0, 0)

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
        
        # Verify benchmark parameters
        self.assertIn("timeIs=Arriving", req.full_url)
        # Date format depends on TflClient implementation, usually YYYYMMDD
        self.assertIn("date=20260303", req.full_url)
        self.assertIn("time=0900", req.full_url)

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

    import json
    @patch("tfl_client.get_next_benchmark_time")
    def test_load_cache_stale_invalidation(self, mock_benchmark_time):
        """Test that _load_cache detects a stale benchmark, deletes the file, and returns None."""
        # Current benchmark time is next Tuesday, e.g. June 2
        mock_benchmark_time.return_value = datetime(2026, 6, 2, 9, 0, 0)
        
        # Write a stale cache entry (benchmark was previous Tuesday, May 26)
        import json
        key = "stale_key"
        cache_path = os.path.join(self.test_cache_dir, f"{key}.json")
        stale_data = {
            "calculated_at": datetime(2026, 5, 20, 12, 0, 0).isoformat(),
            "arrival_benchmark": datetime(2026, 5, 26, 9, 0, 0).isoformat(),
            "response": {"journeys": [{"duration": 25}]}
        }
        with open(cache_path, "w") as f:
            json.dump(stale_data, f)
            
        # Call load cache
        result = self.client._load_cache(key)
        
        # It must return None (stale bypassed) but preserve the file on disk for fallback
        self.assertIsNone(result)
        self.assertTrue(os.path.exists(cache_path))
        
        # Calling with ignore_expiration=True must return the stale data as fallback
        fallback_result = self.client._load_cache(key, ignore_expiration=True)
        self.assertEqual(fallback_result, {"journeys": [{"duration": 25}]})

    @patch("tfl_client.get_next_benchmark_time")
    def test_load_cache_fresh_valid(self, mock_benchmark_time):
        """Test that _load_cache returns cached response when benchmark is still fresh/future."""
        # Current benchmark time is June 2
        mock_benchmark_time.return_value = datetime(2026, 6, 2, 9, 0, 0)
        
        # Write a fresh cache entry (benchmark is also June 2)
        import json
        key = "fresh_key"
        cache_path = os.path.join(self.test_cache_dir, f"{key}.json")
        fresh_data = {
            "calculated_at": datetime(2026, 5, 29, 12, 0, 0).isoformat(),
            "arrival_benchmark": datetime(2026, 6, 2, 9, 0, 0).isoformat(),
            "response": {"journeys": [{"duration": 30}]}
        }
        with open(cache_path, "w") as f:
            json.dump(fresh_data, f)
            
        # Call load cache
        result = self.client._load_cache(key)
        
        # It must return the cached response and leave the file intact
        self.assertEqual(result, {"journeys": [{"duration": 30}]})
        self.assertTrue(os.path.exists(cache_path))

    @patch("tfl_client.get_next_benchmark_time")
    def test_cleanup_stale_caches(self, mock_benchmark_time):
        """Test that cleanup_stale_caches scans the cache dir and deletes expired entries."""
        from tfl_client import cleanup_stale_caches
        
        # Current benchmark time is June 2
        mock_benchmark_time.return_value = datetime(2026, 6, 2, 9, 0, 0)
        
        # 1. Create a stale file (benchmark May 26)
        stale_path = os.path.join(self.test_cache_dir, "stale_entry.json")
        stale_data = {
            "arrival_benchmark": datetime(2026, 5, 26, 9, 0, 0).isoformat(),
            "response": {"journeys": []}
        }
        with open(stale_path, "w") as f:
            json.dump(stale_data, f)
            
        # 2. Create a fresh file (benchmark June 2)
        fresh_path = os.path.join(self.test_cache_dir, "fresh_entry.json")
        fresh_data = {
            "arrival_benchmark": datetime(2026, 6, 2, 9, 0, 0).isoformat(),
            "response": {"journeys": []}
        }
        with open(fresh_path, "w") as f:
            json.dump(fresh_data, f)
            
        # 3. Create a malformed file
        malformed_path = os.path.join(self.test_cache_dir, "malformed.json")
        with open(malformed_path, "w") as f:
            f.write("{invalid_json")
            
        # Call cleanup_stale_caches
        cleanup_stale_caches(self.test_cache_dir)
        
        # Verify stale and malformed files are deleted, fresh remains
        self.assertFalse(os.path.exists(stale_path))
        self.assertFalse(os.path.exists(malformed_path))
        self.assertTrue(os.path.exists(fresh_path))

if __name__ == "__main__":
    unittest.main()
