import unittest
from unittest.mock import patch, MagicMock
from amenity_client import AmenityClient
import json
import os
import shutil

class TestAmenityClient(unittest.TestCase):
    def setUp(self):
        self.test_cache = ".test_cache_client"
        if os.path.exists(self.test_cache):
            shutil.rmtree(self.test_cache)

    def tearDown(self):
        if os.path.exists(self.test_cache):
            shutil.rmtree(self.test_cache)

    def test_fetch_amenities_success(self):
        """Test successful fetching of amenities."""
        expected_json = {
            "elements": [
                {
                    "type": "node",
                    "id": 123,
                    "lat": 51.5,
                    "lon": -0.1,
                    "tags": {"shop": "supermarket", "name": "Sainsbury's"}
                }
            ]
        }
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(expected_json).encode('utf-8')
            mock_urlopen.return_value.__enter__.return_value = mock_response
            
            client = AmenityClient(cache_dir=self.test_cache)
            # Fetch supermarkets within 1000m
            amenities = client.fetch_amenities(51.5, -0.1, 1000, "supermarket")
            
            self.assertEqual(len(amenities), 1)
            self.assertEqual(amenities[0]['name'], "Sainsbury's")
            self.assertAlmostEqual(amenities[0]['distance'], 0.0, delta=1)
            
            # Verify URL call arguments
            self.assertTrue(mock_urlopen.called)

    def test_fetch_amenities_empty(self):
        """Test fetching when no amenities are found."""
        expected_json = {"elements": []}
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(expected_json).encode('utf-8')
            mock_urlopen.return_value.__enter__.return_value = mock_response
            
            client = AmenityClient(cache_dir=self.test_cache)
            amenities = client.fetch_amenities(51.5, -0.1, 1000, "supermarket")
            
            self.assertEqual(len(amenities), 0)

    def test_fetch_amenities_error(self):
        """Test handling of API errors."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = Exception("API Error")
            
            client = AmenityClient(cache_dir=self.test_cache)
            amenities = client.fetch_amenities(51.5, -0.1, 1000, "supermarket")
            
            self.assertEqual(len(amenities), 0) # Should return empty list on error

    def test_fetch_amenities_retry_success(self):
        """Test that client retries on transient failure and eventually succeeds."""
        import urllib.error
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps({"elements": []}).encode('utf-8')
            mock_response.__enter__.return_value = mock_response
            
            # Fail once with URLError, then succeed
            mock_urlopen.side_effect = [urllib.error.URLError("Transient Fail"), mock_response]
            
            client = AmenityClient(cache_dir=self.test_cache)
            with patch('time.sleep'): # Don't actually wait in tests
                amenities = client.fetch_amenities(51.5, -0.1, 1000, "supermarket")
            
            self.assertEqual(mock_urlopen.call_count, 2)
            self.assertEqual(len(amenities), 0)

if __name__ == '__main__':
    unittest.main()
