import unittest
from reporter import Reporter

class TestReporterRefresh(unittest.TestCase):
    def test_generate_commute_cell_with_timestamp(self):
        """Test commute cell includes timestamp if present."""
        reporter = Reporter()
        prop = {
            'commute_time': 30, 
            'commute_cycling': 20, 
            'commute_updated_at': '2026-03-03T09:00:00',
            'latitude': 51.5,
            'longitude': -0.1
        }
        
        # We need to expose _generate_commute_cell or test public method
        # It's private but we can test it
        html = reporter._generate_commute_cell(prop, for_html=True)
        
        # We expect some formatted time or raw ISO for now
        self.assertTrue('09:00' in html or '2026-03-03' in html)

    def test_refresh_icon_present(self):
        """Test refresh icon is present in commute stack."""
        reporter = Reporter()
        prop = {'id': '123', 'commute_time': 30, 'latitude': 51.5, 'longitude': -0.1}
        html = reporter._generate_commute_cell(prop, for_html=True)
        
        # Looking for refresh button/icon
        # Using double quotes for outer string to handle single quotes inside
        expected = "refreshProperty('123')"
        self.assertIn(expected, html)

if __name__ == '__main__':
    unittest.main()
