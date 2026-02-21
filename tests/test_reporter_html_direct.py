import unittest
from reporter import Reporter

class TestReporterDirectHTML(unittest.TestCase):
    def test_generate_html_report_structure(self):
        """Test that generate_html_report builds a valid HTML table."""
        reporter = Reporter()
        props = [{'id': '1', 'price': '100', 'note': 'test'}]
        
        html = reporter.generate_html_report(props)
        self.assertIn("<table>", html)
        self.assertIn("<tr>", html)
        self.assertIn("<td>", html)
        self.assertIn("test", html)
        self.assertIn("<th>Notes</th>", html)

if __name__ == '__main__':
    unittest.main()
