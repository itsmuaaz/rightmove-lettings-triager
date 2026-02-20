import unittest
from unittest.mock import patch
from reporter import Reporter

class TestReporter(unittest.TestCase):
    def test_generate_markdown_row(self):
        property_data = {
            'image_url': 'http://example.com/img.jpg',
            'price': '£2,000 pcm',
            'commute_time': 15,
            'distance': 1.5,
            'bedrooms': 2,
            'type': 'Flat',
            'address': 'Test St',
            'published_on': '2023-10-27T10:00:00Z',
            'url': '/prop/1'
        }
        
        reporter = Reporter()
        # Mock formatted date for consistent testing
        with patch('reporter.format_date', return_value='Today'):
            row = reporter._generate_row(property_data)
            
        self.assertIn('<img src="http://example.com/img.jpg"', row)
        self.assertIn('£2,000 pcm', row)
        self.assertIn('badge-green', row) # 15 mins should be green
        self.assertIn('1.50 mi', row)
        self.assertIn('2 bed Flat', row)
        self.assertIn('Test St', row)
        self.assertIn('Today', row)
        self.assertIn('(https://www.rightmove.co.uk/prop/1)', row)

    def test_get_commute_class(self):
        reporter = Reporter()
        self.assertEqual(reporter._get_commute_class(None), "badge-grey")
        self.assertEqual(reporter._get_commute_class("invalid"), "badge-grey")
        self.assertEqual(reporter._get_commute_class(15), "badge-green")
        self.assertEqual(reporter._get_commute_class(20), "badge-amber")
        self.assertEqual(reporter._get_commute_class(40), "badge-amber")
        self.assertEqual(reporter._get_commute_class(45), "badge-red")

    def test_generate_markdown(self):
        reporter = Reporter()
        props = [
            {'price': '£100', 'commute_time': 10},
            {'price': '£200', 'commute_time': 50}
        ]
        with patch('reporter.format_date', return_value='Today'):
            md = reporter.generate_markdown(props)
            
        self.assertIn("| Image | Price | Commute", md)
        self.assertIn("---", md)
        self.assertIn("£100", md)
        self.assertIn("badge-green", md)
        self.assertIn("£200", md)
        self.assertIn("badge-red", md)

if __name__ == '__main__':
    unittest.main()
