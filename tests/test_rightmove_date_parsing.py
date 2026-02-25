import unittest
from rightmove_search import parse_property_data

class TestRightmoveDateParsing(unittest.TestCase):
    def test_parse_first_visible_date(self):
        """Test that firstVisibleDate is correctly mapped to published_on."""
        raw_property = {
            'id': '12345',
            'price': {'displayPrices': [{'displayPrice': '£1,500 pcm'}]},
            'propertyTypeFullDescription': 'Flat',
            'displayAddress': 'Test Address',
            'customer': {'brandTradingName': 'Test Agent'},
            'propertyUrl': '/prop/12345',
            'firstVisibleDate': '2026-02-19T13:54:46Z',
            'firstPublishedDate': None  # Simulate missing field
        }
        
        parsed = parse_property_data(raw_property)
        self.assertEqual(parsed['published_on'], '2026-02-19T13:54:46Z')

    def test_fallback_to_listing_update_date(self):
        """Test fallback to listingUpdateDate if firstVisibleDate is missing."""
        raw_property = {
            'id': '12345',
            'price': {'displayPrices': [{'displayPrice': '£1,500 pcm'}]},
            'firstVisibleDate': None,
            'listingUpdate': {
                'listingUpdateDate': '2026-02-20T10:00:00Z'
            }
        }
        
        parsed = parse_property_data(raw_property)
        self.assertEqual(parsed['published_on'], '2026-02-20T10:00:00Z')

    def test_no_date_available(self):
        """Test that published_on is None if no date is found."""
        raw_property = {
            'id': '12345',
            'price': {'displayPrices': [{'displayPrice': '£1,500 pcm'}]},
        }
        
        parsed = parse_property_data(raw_property)
        self.assertIsNone(parsed['published_on'])

if __name__ == "__main__":
    unittest.main()
