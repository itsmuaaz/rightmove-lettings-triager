import unittest
from datetime import datetime, timedelta
from utils import format_date

class TestDateUtils(unittest.TestCase):
    def test_format_date_recent(self):
        # Test "2 days ago"
        now = datetime.now()
        past = now - timedelta(days=2)
        # Assuming format_date accepts ISO string
        iso_str = past.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.assertEqual(format_date(iso_str), '2 days ago')

    def test_format_date_today(self):
        now = datetime.now()
        iso_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.assertEqual(format_date(iso_str), 'Today')

    def test_format_date_invalid(self):
        self.assertEqual(format_date(None), 'Unknown')
        self.assertEqual(format_date('invalid-date'), 'Unknown')

if __name__ == '__main__':
    unittest.main()
