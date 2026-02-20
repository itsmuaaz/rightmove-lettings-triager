import unittest
from rightmove_search import parse_property_data

class TestParser(unittest.TestCase):
    def test_parse_property_data_complete(self):
        raw_property = {
            'price': {'displayPrices': [{'displayPrice': '£2,500 pcm'}]},
            'propertyTypeFullDescription': '2 bedroom flat',
            'displayAddress': 'Test Street, London',
            'customer': {'brandTradingName': 'Test Agent'},
            'propertyUrl': '/properties/12345',
            'location': {'latitude': 51.5, 'longitude': -0.1},
            'propertyImages': {'images': [{'srcUrl': 'http://example.com/image.jpg'}]},
            'bedrooms': 2,
            'firstPublishedDate': '2023-10-27T10:00:00Z',
            'summary': 'A lovely flat.'
        }

        parsed = parse_property_data(raw_property)

        self.assertEqual(parsed['price'], '£2,500 pcm')
        self.assertEqual(parsed['type'], '2 bedroom flat')
        self.assertEqual(parsed['address'], 'Test Street, London')
        self.assertEqual(parsed['agent'], 'Test Agent')
        self.assertEqual(parsed['url'], '/properties/12345')
        self.assertEqual(parsed['image_url'], 'http://example.com/image.jpg')
        self.assertEqual(parsed['bedrooms'], 2)
        self.assertEqual(parsed['published_on'], '2023-10-27T10:00:00Z')
        self.assertEqual(parsed['summary'], 'A lovely flat.')
        self.assertEqual(parsed['latitude'], 51.5)
        self.assertEqual(parsed['longitude'], -0.1)

    def test_parse_property_data_missing_fields(self):
        raw_property = {}
        parsed = parse_property_data(raw_property)
        
        self.assertEqual(parsed['price'], 'N/A')
        self.assertEqual(parsed['image_url'], None)
        self.assertEqual(parsed['bedrooms'], 0)
        self.assertEqual(parsed['published_on'], None)

if __name__ == '__main__':
    unittest.main()
