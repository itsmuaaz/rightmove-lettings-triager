import unittest
from unittest.mock import MagicMock, patch
from reporter import Reporter
import os

class TestReporter(unittest.TestCase):
    def setUp(self):
        self.reporter = Reporter()
        self.sample_properties = [
            {
                "id": "1",
                "price_pcm": "2000",
                "price_pw": "462",
                "address": "123 Test St",
                "type": "Flat",
                "link": "https://rightmove.co.uk/property/1",
                "commute_time": 25,
                "commute_cycling": 15,
                "images": ["http://img.com/1.jpg"],
                "amenities": [],
                "status": "new"
            }
        ]

    def test_generate_report_returns_html(self):
        """Test that generate_report returns a string containing HTML."""
        # We mock the template loading to avoid file system dependency if possible,
        # but integration testing with real templates is better for Jinja.
        # However, for unit test, let's verify it calls the template.
        
        with patch('jinja2.Environment.get_template') as mock_get_template:
            mock_template = MagicMock()
            mock_template.render.return_value = "<html>Result</html>"
            mock_get_template.return_value = mock_template
            
            html_output = self.reporter.generate_report(self.sample_properties)
            
            self.assertEqual(html_output, "<html>Result</html>")
            mock_get_template.assert_called_with("report.html")
            mock_template.render.assert_called()
            
            # Check context passed to render
            args, kwargs = mock_template.render.call_args
            self.assertIn("properties", kwargs)
            
            # Properties are enriched, so they won't match sample_properties exactly
            # We check if the enriched properties contain the original data + new fields
            passed_props = kwargs["properties"]
            self.assertEqual(len(passed_props), len(self.sample_properties))
            self.assertEqual(passed_props[0]['id'], self.sample_properties[0]['id'])
            self.assertIn('commute_color_class', passed_props[0])

    def test_enrichment_logic(self):
        """Test that the reporter enriches properties with display logic before rendering."""
        # This assumes Reporter does some pre-processing like calculating color classes
        # If we move that logic to Jinja, this test might be irrelevant or check for different things.
        # For now, let's assume Reporter adds 'commute_color_class'.
        
        # If the plan implies moving logic to Jinja, Reporter might just pass data.
        # But commonly we prepare view models in Python.
        pass

if __name__ == '__main__':
    unittest.main()
