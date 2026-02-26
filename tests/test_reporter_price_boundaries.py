import unittest
from reporter import Reporter

class TestReporterPriceIndicator(unittest.TestCase):
    def test_calculate_min_max_prices(self):
        reporter = Reporter()
        properties = [
            {'id': '1', 'price': '£1,000 pcm'},
            {'id': '2', 'price': '£2,000 pcm'},
            {'id': '3', 'price': 'POA'},
            {'id': '4', 'price': '£1,500 pcm'}
        ]
        
        # We need to test the logic that happens inside generate_report or extract it.
        # Let's extract the min/max calculation to a helper method on Reporter
        # so we can test it directly.
        min_p, max_p = reporter._calculate_price_boundaries(properties)
        
        self.assertEqual(min_p, 1000)
        self.assertEqual(max_p, 2000)

if __name__ == '__main__':
    unittest.main()
