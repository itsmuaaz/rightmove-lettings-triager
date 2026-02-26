import unittest
import os
import json
from scoring import SmartScorer
from config_manager import ConfigManager

class TestSmartScorerIntegration(unittest.TestCase):
    def setUp(self):
        # Create a temporary config file
        self.test_config_file = ".scoring_config.json"
        self.manager = ConfigManager(config_file=self.test_config_file, defaults={})
        
        # Save custom weights: Price 100%
        self.custom_weights = {"price": 1.0, "commute": 0.0, "vibe": 0.0, "freshness": 0.0}
        self.manager.save_config(self.custom_weights)

    def tearDown(self):
        if os.path.exists(self.test_config_file):
            os.remove(self.test_config_file)

    def test_smart_scorer_uses_saved_config(self):
        # Initialize scorer (should load from file via config.py -> ConfigManager)
        scorer = SmartScorer()
        
        # Verify weights
        self.assertAlmostEqual(scorer.weights["price"], 1.0)
        self.assertAlmostEqual(scorer.weights["commute"], 0.0)

    def test_smart_scorer_calculation_with_custom_weights(self):
        scorer = SmartScorer()
        
        # Property with bad price but good everything else
        # Since Price weight is 100%, score should be determined solely by price.
        # But wait, normalization.
        
        property_data = {
            "price": "£1000 pcm",
            "commute_time": 0, # Perfect
            "vibe": {"score": 10}, # Perfect
            "published_on": "2023-10-27T10:00:00Z" # Perfect
        }
        global_stats = {"min_price": 1000, "max_price": 2000}
        
        # Price 1000 is min -> Score 100.
        # Total score = 100 * 1.0 = 100.
        
        # Mock get_days_since to 0
        from unittest.mock import patch
        with patch('scoring.get_days_since', return_value=0):
            score_data = scorer.calculate_score(property_data, global_stats)
            
        self.assertAlmostEqual(score_data['total'], 100.0)
        self.assertAlmostEqual(score_data['breakdown']['price'], 100.0)
        self.assertAlmostEqual(score_data['breakdown']['commute'], 0.0)

if __name__ == "__main__":
    unittest.main()
