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
        # 90+ -> Green
        self.assertIn("bg-green-", enriched.get("smart_score_badge_class", ""))

    def test_enrich_property_medium_score(self):
        p = {"smart_score": 80}
        enriched = self.reporter._enrich_property(p)
        
        self.assertEqual(enriched.get("smart_score"), 80)
        # 70-89 -> Yellow
        self.assertIn("bg-yellow-", enriched.get("smart_score_badge_class", ""))

    def test_enrich_property_low_score(self):
        p = {"smart_score": 50}
        enriched = self.reporter._enrich_property(p)
        
        self.assertEqual(enriched.get("smart_score"), 50)
        # <70 -> Gray or Red? Spec says "Average/Poor" (White circle in spec text? No, earlier I said "Green >90, Yellow >70, Gray <70")
        # Let's check spec details: "🟢 90+, 🟡 70-89, ⚪ <70"
        # ⚪ usually implies Gray or White. Let's use Gray.
        self.assertIn("bg-gray-", enriched.get("smart_score_badge_class", ""))

    def test_enrich_property_no_score(self):
        p = {} # No smart_score
        enriched = self.reporter._enrich_property(p)
        
        self.assertEqual(enriched.get("smart_score"), "N/A")
        self.assertIn("bg-gray-", enriched.get("smart_score_badge_class", ""))

if __name__ == '__main__':
    unittest.main()
