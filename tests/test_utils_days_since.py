import unittest
from datetime import datetime, timedelta
from utils import get_days_since

class TestGetDaysSince(unittest.TestCase):
    def test_get_days_since_today(self):
        """Test that get_days_since returns 0 for today's date."""
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(get_days_since(today), 0)

    def test_get_days_since_yesterday(self):
        """Test that get_days_since returns 1 for yesterday's date."""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(get_days_since(yesterday), 1)

    def test_get_days_since_past(self):
        """Test that get_days_since returns correct days for a past date."""
        past_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        self.assertEqual(get_days_since(past_date), 5)
    
    def test_get_days_since_iso_format(self):
        """Test with ISO format including time."""
        dt = datetime.now() - timedelta(days=2)
        iso_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
        self.assertEqual(get_days_since(iso_date), 2)

    def test_get_days_since_none(self):
        """Test that get_days_since returns None for None input."""
        self.assertIsNone(get_days_since(None))

    def test_get_days_since_invalid(self):
        """Test that get_days_since returns None for invalid date string."""
        self.assertIsNone(get_days_since("not-a-date"))

if __name__ == '__main__':
    unittest.main()
