import unittest
from reporter import Reporter

class TestReporterProgressive(unittest.TestCase):
    def setUp(self):
        self.reporter = Reporter()
    
    def test_enrich_property_with_none_values(self):
        # Property with no processed data yet
        prop = {'id': '1', 'url': '/test', 'address': 'Test St'}
        
        enriched = self.reporter._enrich_property(prop)
        
        self.assertEqual(enriched['commute_time'], "Loading...")
        self.assertEqual(enriched['cycling_time'], "Loading...")
        self.assertEqual(enriched['commute_color_class'], "text-gray-400 italic")
        self.assertEqual(enriched['amenities'], [])
        
        # Verify original property is NOT mutated
        self.assertNotIn('commute_time', prop)
        
    def test_generate_report_accepts_counts(self):
        props = [{'id': '1', 'url': '/test', 'address': 'Test St'}]
        # This shouldn't crash
        html = self.reporter.generate_report(props, processed_count=5, total_count=10)
        self.assertIn('5', html)
        self.assertIn('10', html)

if __name__ == '__main__':
    unittest.main()
