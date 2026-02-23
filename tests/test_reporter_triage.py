import unittest
from reporter import Reporter

class TestReporterTriage(unittest.TestCase):
    def test_generate_html_row_shortlisted(self):
        """Test that a shortlisted property gets the correct row class and button."""
        property_data = {
            'id': 'prop1',
            'price': '£1,500',
            'history_status': {'status': 'shortlisted'}
        }
        
        reporter = Reporter()
        row_html = reporter._generate_html_row(property_data)
        
        # Verify row class
        self.assertIn('class="prop-row status-shortlisted"', row_html)
        # Verify Shortlist button is present
        self.assertIn('btn-shortlist', row_html)
        self.assertIn('⭐ Shortlist', row_html)
        # Verify other buttons
        self.assertIn('btn-view', row_html)
        self.assertIn('btn-dismiss', row_html)

    def test_generate_html_row_new(self):
        """Test that a new property gets the correct row class and button."""
        property_data = {
            'id': 'prop2',
            'price': '£1,200',
            'history_status': {'status': 'new'}
        }
        
        reporter = Reporter()
        row_html = reporter._generate_html_row(property_data)
        
        self.assertIn('class="prop-row status-new"', row_html)
        self.assertIn('badge-new', row_html)
        self.assertIn('⭐ Shortlist', row_html)

if __name__ == '__main__':
    unittest.main()
