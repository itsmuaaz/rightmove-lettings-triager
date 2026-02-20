import unittest
from unittest.mock import patch, MagicMock
from amenity_client import AmenityClient
import json
import os
import shutil
import urllib.error

class TestAmenityClient(unittest.TestCase):
    def setUp(self):
        self.test_cache = ".test_cache_client"
        if os.path.exists(self.test_cache):
            shutil.rmtree(self.test_cache)

    def tearDown(self):
        if os.path.exists(self.test_cache):
            shutil.rmtree(self.test_cache)

    def test_fetch_all_amenities_success(self):
        """Test successful bulk fetching of amenities."""
        expected_json = {
            "elements": [
                {
                    "type": "node",
                    "id": 1,
                    "lat": 51.5,
                    "lon": -0.1,
                    "tags": {"shop": "supermarket", "name": "Sainsbury's"}
                },
                {
                    "type": "node",
                    "id": 2,
                    "lat": 51.501,
                    "lon": -0.101,
                    "tags": {"leisure": "fitness_centre", "name": "PureGym"}
                }
            ]
        }
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(expected_json).encode('utf-8')
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response
            
            client = AmenityClient(cache_dir=self.test_cache)
            results = client.fetch_all_amenities(51.5, -0.1, 1000)
            
            self.assertEqual(len(results['supermarket']), 1)
            self.assertEqual(results['supermarket'][0]['name'], "Sainsbury's")
            self.assertEqual(len(results['gym']), 1)
            self.assertEqual(results['gym'][0]['name'], "PureGym")
            
    def test_fetch_all_amenities_empty(self):
        """Test bulk fetching when no amenities are found."""
        expected_json = {"elements": []}
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(expected_json).encode('utf-8')
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response
            
            client = AmenityClient(cache_dir=self.test_cache)
            results = client.fetch_all_amenities(51.5, -0.1, 1000)
            
            self.assertEqual(len(results['supermarket']), 0)

    def test_fetch_all_amenities_retry_success(self):
        """Test retry logic: fail once, then succeed."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps({"elements": []}).encode('utf-8')
            mock_response.__enter__.return_value = mock_response
            
            # Fail once with URLError, then succeed
            mock_urlopen.side_effect = [urllib.error.URLError("Fail"), mock_response]
            
            client = AmenityClient(cache_dir=self.test_cache)
            with patch('time.sleep'):
                results = client.fetch_all_amenities(51.5, -0.1, 1000)
            
            self.assertEqual(mock_urlopen.call_count, 2)
            self.assertIsNotNone(results)
            self.assertIn('supermarket', results)

    def test_fetch_all_amenities_retry_failure(self):
        """Test retry logic: fail always -> return None."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            # Always fail
            mock_urlopen.side_effect = urllib.error.URLError("Fail")
            
            client = AmenityClient(cache_dir=self.test_cache)
            with patch('time.sleep'):
                results = client.fetch_all_amenities(51.5, -0.1, 1000)
            
            # Should try 3 times (default max_attempts)
            self.assertEqual(mock_urlopen.call_count, 3)
            self.assertIsNone(results)

if __name__ == '__main__':
    unittest.main()
