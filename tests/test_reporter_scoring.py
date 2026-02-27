import unittest
from reporter import Reporter
from unittest.mock import MagicMock

class TestReporterScoring(unittest.TestCase):
    def setUp(self):
        # We can pass a dummy template dir, or mock the env
        self.reporter = Reporter(template_dir="templates")
    
    def test_enrich_property_high_score(self):
        p = {"smart_score": 95}
        enriched = self.reporter._enrich_property(p)
        
        self.assertEqual(enriched.get("smart_score"), 95)
        # 90+ -> Green (Hue 120)
        self.assertIn("hsl(120,", enriched.get("smart_score_bg_color", ""))
        self.assertIn("inline-flex", enriched.get("smart_score_badge_class", ""))

    def test_enrich_property_medium_score(self):
        p = {"smart_score": 80}
        enriched = self.reporter._enrich_property(p)
        
        self.assertEqual(enriched.get("smart_score"), 80)
        # 80 -> Green (Hue 120)
        self.assertIn("hsl(120,", enriched.get("smart_score_bg_color", ""))

    def test_enrich_property_low_score(self):
        p = {"smart_score": 50}
        enriched = self.reporter._enrich_property(p)
        
        self.assertEqual(enriched.get("smart_score"), 50)
        # 50 -> Mix (Hue 60)
        self.assertIn("hsl(60,", enriched.get("smart_score_bg_color", ""))

    def test_enrich_property_no_score(self):
        p = {} # No smart_score
        enriched = self.reporter._enrich_property(p)
        
        self.assertEqual(enriched.get("smart_score"), "N/A")
        # Default gray
        self.assertEqual(enriched.get("smart_score_bg_color"), "#D1D5DB")

if __name__ == '__main__':
    unittest.main()
