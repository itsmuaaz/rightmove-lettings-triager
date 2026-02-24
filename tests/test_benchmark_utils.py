import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from benchmark_utils import get_next_benchmark_time

class TestBenchmarkUtils(unittest.TestCase):

    def test_next_tuesday_from_monday(self):
        # Monday 2026-02-23 10:00:00 -> Next Tuesday 2026-02-24 09:00:00
        mock_now = datetime(2026, 2, 23, 10, 0, 0)
        with patch('benchmark_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_now
            mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
            
            result = get_next_benchmark_time()
            expected = datetime(2026, 2, 24, 9, 0, 0)
            self.assertEqual(result, expected)

    def test_today_tuesday_before_9am(self):
        # Tuesday 2026-02-24 08:00:00 -> Today Tuesday 2026-02-24 09:00:00
        mock_now = datetime(2026, 2, 24, 8, 0, 0)
        with patch('benchmark_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_now
            mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
            
            result = get_next_benchmark_time()
            expected = datetime(2026, 2, 24, 9, 0, 0)
            self.assertEqual(result, expected)

    def test_next_tuesday_from_tuesday_after_9am(self):
        # Tuesday 2026-02-24 10:00:00 -> Next Tuesday 2026-03-03 09:00:00
        mock_now = datetime(2026, 2, 24, 10, 0, 0)
        with patch('benchmark_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_now
            mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
            
            result = get_next_benchmark_time()
            expected = datetime(2026, 3, 3, 9, 0, 0)
            self.assertEqual(result, expected)

    def test_next_tuesday_from_wednesday(self):
        # Wednesday 2026-02-25 10:00:00 -> Next Tuesday 2026-03-03 09:00:00
        mock_now = datetime(2026, 2, 25, 10, 0, 0)
        with patch('benchmark_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_now
            mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
            
            result = get_next_benchmark_time()
            expected = datetime(2026, 3, 3, 9, 0, 0)
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
