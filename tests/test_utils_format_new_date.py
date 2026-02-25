import unittest
from datetime import datetime, timedelta
from utils import format_date

class TestUtilsFormatNewDate(unittest.TestCase):
    def test_format_rightmove_date(self):
        """Test formatting of Rightmove's firstVisibleDate format."""
        # Create a date that is 5 days ago relative to now
        now = datetime.now()
        past = now - timedelta(days=5)
        
        # Format: 2026-02-19T13:54:46Z
        iso_str = past.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Should return "5 days ago"
        self.assertEqual(format_date(iso_str), '5 days ago')

    def test_format_listing_update_date(self):
        """Test formatting of listingUpdateDate format."""
        # Create a date that is 1 day ago (Yesterday)
        now = datetime.now()
        past = now - timedelta(days=1)
        
        # Format: 2026-02-19T14:00:10Z
        iso_str = past.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        self.assertEqual(format_date(iso_str), 'Yesterday')

if __name__ == '__main__':
    unittest.main()
