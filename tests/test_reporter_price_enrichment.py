import unittest
from reporter import Reporter

class TestReporterPriceEnrichment(unittest.TestCase):
    def test_enrich_property_with_price_indicator(self):
        reporter = Reporter()
        p_min = {'id': '1', 'price': '£1,000 pcm'}
        p_mid = {'id': '2', 'price': '£1,500 pcm'}
        p_max = {'id': '3', 'price': '£2,000 pcm'}
        
        # Test min price (Green, hue 120)
        e_min = reporter._enrich_property(p_min, min_price=1000, max_price=2000)
        self.assertEqual(e_min['price_indicator_color'], 'hsl(120, 100%, 45%)')

        # Test max price (Red, hue 0)
        e_max = reporter._enrich_property(p_max, min_price=1000, max_price=2000)
        self.assertEqual(e_max['price_indicator_color'], 'hsl(0, 100%, 45%)')
        
        # Test mid price (Yellow, hue 60)
        e_mid = reporter._enrich_property(p_mid, min_price=1000, max_price=2000)
        self.assertEqual(e_mid['price_indicator_color'], 'hsl(60, 100%, 45%)')

    def test_enrich_property_same_min_max(self):
        reporter = Reporter()
        p = {'id': '1', 'price': '£1,000 pcm'}
        
        e = reporter._enrich_property(p, min_price=1000, max_price=1000)
        self.assertEqual(e['price_indicator_color'], 'hsl(60, 100%, 45%)') # Default to yellow

    def test_enrich_property_no_boundaries(self):
        reporter = Reporter()
        p = {'id': '1', 'price': '£1,000 pcm'}
        
        e = reporter._enrich_property(p, min_price=None, max_price=None)
        self.assertNotIn('price_indicator_color', e)

    def test_enrich_property_invalid_price(self):
        reporter = Reporter()
        p = {'id': '1', 'price': 'POA'}
        
        e = reporter._enrich_property(p, min_price=1000, max_price=2000)
        self.assertNotIn('price_indicator_color', e)

if __name__ == '__main__':
    unittest.main()
