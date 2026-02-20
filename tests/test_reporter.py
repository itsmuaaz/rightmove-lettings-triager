import unittest
from unittest.mock import patch
from reporter import Reporter

class TestReporter(unittest.TestCase):
    def test_generate_markdown_row(self):
        """Test generation of a single Markdown row with correct badges and links."""
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

    def test_generate_markdown_row_dual_commute(self):
        """Test generation of a row with both public transport and cycling times."""
        property_data = {
            'image_url': 'http://example.com/img.jpg',
            'price': '£2,000 pcm',
            'commute_time': 15,
            'commute_cycling': 10,
            'distance': 1.5,
            'bedrooms': 2,
            'type': 'Flat',
            'address': 'Test St',
            'published_on': '2023-10-27T10:00:00Z',
            'url': '/prop/1',
            'latitude': 51.5,
            'longitude': -0.1
        }
        
        reporter = Reporter()
        with patch('reporter.format_date', return_value='Today'):
            with patch('reporter.generate_google_maps_url', return_value='http://gmaps'):
                with patch('reporter.generate_tfl_url', return_value='http://tfl'):
                    # Test Markdown (Inline)
                    row_md = reporter._generate_row(property_data, for_html=False)
                    self.assertIn('15 mins', row_md)
                    self.assertIn('10 mins', row_md)
                    self.assertIn('🚆', row_md)
                    self.assertIn('🚲', row_md)
                    self.assertIn(' / ', row_md) # Separator
                    self.assertIn('[GMaps](http://gmaps)', row_md)
                    self.assertIn('[TfL](http://tfl)', row_md)
                    
                    # Test HTML (Stacked)
                    row_html = reporter._generate_row(property_data, for_html=True)
                    self.assertIn('commute-stack', row_html)
                    self.assertNotIn(' / ', row_html) # No text separator in stacked mode
                    self.assertIn('href="http://gmaps"', row_html)
                    self.assertIn('href="http://tfl"', row_html)

    def test_generate_markdown_row_amenities(self):
        """Test generation of a row with nearby amenities."""
        property_data = {
            'price': '£1,000',
            'nearby_amenities': {
                'supermarket': {'name': 'Tesco', 'distance': 200},
                'gym': {'name': 'PureGym', 'distance': 500}
            }
        }
        
        reporter = Reporter()
        with patch('reporter.format_date', return_value='Today'):
            with patch('reporter.generate_google_maps_url', return_value=''):
                with patch('reporter.generate_tfl_url', return_value=''):
                    row = reporter._generate_row(property_data)
                    
        # 200m / 80 = 2.5 -> 2 mins. 500m / 80 = 6.25 -> 6 mins
        self.assertIn('🛒 Tesco (~2 mins)', row)
        self.assertIn('💪 PureGym (~6 mins)', row)
        self.assertIn('🌳 None nearby', row)

    def test_generate_markdown_row_amenities_error(self):
        """Test generation of a row when amenities calculation failed."""
        property_data = {
            'price': '£1,000',
            'nearby_amenities': None
        }
        
        reporter = Reporter()
        with patch('reporter.format_date', return_value='Today'):
            with patch('reporter.generate_google_maps_url', return_value=''):
                with patch('reporter.generate_tfl_url', return_value=''):
                    row = reporter._generate_row(property_data)
                    
        self.assertIn('⚠ Data Error', row)

    def test_get_commute_class(self):
        """Test logic for assigning traffic light CSS classes to commute times."""
        reporter = Reporter()
        self.assertEqual(reporter._get_commute_class(None), "badge-grey")
        self.assertEqual(reporter._get_commute_class("invalid"), "badge-grey")
        self.assertEqual(reporter._get_commute_class(15), "badge-green")
        self.assertEqual(reporter._get_commute_class(20), "badge-amber")
        self.assertEqual(reporter._get_commute_class(40), "badge-amber")
        self.assertEqual(reporter._get_commute_class(45), "badge-red")

    def test_generate_markdown(self):
        """Test full Markdown report generation."""
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

    def test_get_html_template(self):
        """Test retrieval of the HTML template with embedded CSS."""
        reporter = Reporter()
        html = reporter.get_html_template()
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn(".badge-green", html)
        self.assertIn(".prop-img", html)
        self.assertIn("background-color: #d4edda", html) # Green background

    def test_convert_to_html(self):
        """Test conversion of Markdown content to HTML using the template."""
        reporter = Reporter()
        md_content = "| H1 | H2 |\n|---|---|\n| C1 | C2 |"
        html = reporter.convert_to_html(md_content)
        
        self.assertIn("<table>", html)
        self.assertIn("<thead>", html)
        self.assertIn("<tbody>", html)
        self.assertIn("<td>C1</td>", html)
        self.assertIn("background-color: #d4edda", html) # Ensure template is applied

    def test_sanitize_newlines(self):
        """Test sanitization of newlines in property data to prevent broken tables."""
        property_data = {
            'price': '£100',
            'address': 'Line 1\nLine 2',
            'commute_time': 10
        }
        reporter = Reporter()
        with patch('reporter.format_date', return_value='Today'):
            row = reporter._generate_row(property_data)
        
        self.assertNotIn('\n', row.split('|')[6]) # Address column
        self.assertIn('Line 1 Line 2', row)

if __name__ == '__main__':
    unittest.main()
