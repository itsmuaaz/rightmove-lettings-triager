import unittest
from reporter import Reporter

class TestReporterFares(unittest.TestCase):
    def setUp(self):
        self.reporter = Reporter()

    def test_enrich_property_with_fares(self):
        prop = {
            'id': '1',
            'commute_time': 45,
            'commute_fares': {'peak': 350, 'off_peak': 280},
            'location': {'latitude': 51.5, 'longitude': -0.1}
        }
        enriched = self.reporter._enrich_property(prop)
        # Check if commute_cost_display is present and formatted correctly
        self.assertIn('commute_cost_display', enriched)
        # Expected format: "£3.50 / £2.80"
        self.assertEqual(enriched['commute_cost_display'], "£3.50 / £2.80")

    def test_enrich_property_with_single_fare(self):
        prop = {
            'id': '2',
            'commute_time': 30,
            'commute_fares': {'total_cost': 150}, # Only total cost
            'location': {'latitude': 51.5, 'longitude': -0.1}
        }
        enriched = self.reporter._enrich_property(prop)
        self.assertEqual(enriched['commute_cost_display'], "£1.50")

    def test_enrich_property_without_fares(self):
        prop = {
            'id': '3',
            'commute_time': 30,
            'commute_fares': None,
            'location': {'latitude': 51.5, 'longitude': -0.1}
        }
        enriched = self.reporter._enrich_property(prop)
        self.assertNotIn('commute_cost_display', enriched)

if __name__ == "__main__":
    unittest.main()
