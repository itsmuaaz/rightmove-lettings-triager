import unittest
from unittest.mock import patch, MagicMock
from utils import extract_postcode_district, extract_location_for_vibe, get_sort_key, reverse_geocode

class TestUtilsVibe(unittest.TestCase):
    def test_extract_postcode_district(self):
        self.assertEqual(extract_postcode_district("123 High St, SW14 7AB"), "SW14")
        self.assertEqual(extract_postcode_district("Flat 1, E1 6AN"), "E1")
        self.assertEqual(extract_postcode_district("N1C 4AG"), "N1C")
        self.assertEqual(extract_postcode_district("No Postcode Here"), None)
        self.assertEqual(extract_postcode_district(""), None)
        self.assertEqual(extract_postcode_district(None), None)

    def test_extract_location_for_vibe(self):
        # Postcode present
        self.assertEqual(extract_location_for_vibe("123 High St, SW14 7AB"), "SW14")
        
        # Postcode missing, return cleaned address (with no coords)
        self.assertEqual(extract_location_for_vibe("Mazenod Avenue, West Hampstead"), "Mazenod Avenue, West Hampstead")
        
        # Empty/None
        self.assertEqual(extract_location_for_vibe(""), None)
        self.assertEqual(extract_location_for_vibe(None), None)
        self.assertEqual(extract_location_for_vibe("   "), None)

    @patch("urllib.request.urlopen")
    def test_reverse_geocode_success(self, mock_urlopen):
        """Test reverse geocoding returns correct district on successful response."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"status": 200, "result": [{"outcode": "WC2N"}]}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        # Clear geocode cache before test
        import utils
        utils._GEOCODE_CACHE = {}
        
        district = reverse_geocode(51.5074, -0.1278)
        self.assertEqual(district, "WC2N")
        
    @patch("urllib.request.urlopen")
    def test_reverse_geocode_timeout_or_error(self, mock_urlopen):
        """Test reverse geocoding returns None gracefully on timeouts or HTTP errors."""
        mock_urlopen.side_effect = Exception("Timeout error")
        
        # Clear geocode cache before test to prevent state pollution
        import utils
        utils._GEOCODE_CACHE = {}
        
        district = reverse_geocode(51.1111, -0.2222)
        self.assertIsNone(district)

    @patch("urllib.request.urlopen")
    def test_reverse_geocode_caching(self, mock_urlopen):
        """Test that reverse_geocode caches results and does not make duplicate requests."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"status": 200, "result": [{"outcode": "SW15"}]}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        # Clear geocode cache
        import utils
        utils._GEOCODE_CACHE = {}
        
        # Query same coordinates twice
        d1 = reverse_geocode(51.465, -0.22)
        d2 = reverse_geocode(51.465, -0.22)
        
        self.assertEqual(d1, "SW15")
        self.assertEqual(d2, "SW15")
        self.assertEqual(mock_urlopen.call_count, 1) # API should only be called once!

    @patch("utils.reverse_geocode")
    def test_extract_location_for_vibe_fallback_with_coords(self, mock_reverse):
        """Test that extract_location_for_vibe falls back to reverse-geocoding if address is descriptive."""
        mock_reverse.return_value = "SW15"
        
        # Address has no postcode district, but has valid coordinates
        result = extract_location_for_vibe("2 bedroom flat", (51.465, -0.22))
        
        self.assertEqual(result, "SW15")
        mock_reverse.assert_called_once_with(51.465, -0.22)

    def test_get_sort_key(self):
        # Both present
        self.assertEqual(get_sort_key({'commute_time': 30, 'commute_cycling': 40}), 30)
        self.assertEqual(get_sort_key({'commute_time': 50, 'commute_cycling': 40}), 40)
        
        # One present
        self.assertEqual(get_sort_key({'commute_time': 30, 'commute_cycling': None}), 30)
        self.assertEqual(get_sort_key({'commute_time': None, 'commute_cycling': 40}), 40)
        
        # None present
        self.assertEqual(get_sort_key({'commute_time': None, 'commute_cycling': None}), float('inf'))

if __name__ == '__main__':
    unittest.main()
