import unittest
from unittest.mock import patch, MagicMock
from scoring import SmartScorer

class TestSmartScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = SmartScorer()
        # Mock configuration for predictable testing
        self.scorer.weights = {
            "price": 0.3,
            "commute": 0.4,
            "vibe": 0.2,
            "freshness": 0.1
        }
        self.scorer.max_commute = 60
        self.scorer.freshness_decay = 7

    def test_calculate_score_perfect_property(self):
        """Test a property with best possible values gets 100."""
        # Cheapest price (matches min), 0 commute, 10/10 vibe, listed today (0 days)
        property_data = {
            "price": "£1,000 pcm",
            "commute_time": 0,
            "vibe_score": 10,
            "published_on": "2023-10-27T10:00:00Z" # Mocked 'today' in utils would be needed or just pass 0 days
        }
        global_stats = {"min_price": 1000, "max_price": 2000}
        
        with patch('scoring.get_days_since', return_value=0):
             score_data = self.scorer.calculate_score(property_data, global_stats)
        
        self.assertAlmostEqual(score_data['total'], 100.0)
        self.assertAlmostEqual(score_data['breakdown']['price'], 30.0)     # 100 * 0.3
        self.assertAlmostEqual(score_data['breakdown']['commute'], 40.0)   # 100 * 0.4
        self.assertAlmostEqual(score_data['breakdown']['vibe'], 20.0)      # 100 * 0.2
        self.assertAlmostEqual(score_data['breakdown']['freshness'], 10.0) # 100 * 0.1

    def test_calculate_score_worst_property(self):
        """Test a property with worst possible values gets 0."""
        # Most expensive, >60 commute, 0 vibe, >7 days old
        property_data = {
            "price": "£2,000 pcm",
            "commute_time": 61,
            "vibe_score": 1, # Vibe 1 scales to 0? Or 1/10? Spec says 1-10. Let's assume linear mapping 1->0, 10->100
            "published_on": "2023-10-01T10:00:00Z"
        }
        global_stats = {"min_price": 1000, "max_price": 2000}
        
        with patch('scoring.get_days_since', return_value=8):
             score_data = self.scorer.calculate_score(property_data, global_stats)
        
        # Price: 0 (max price)
        # Commute: 0 (>60 mins)
        # Vibe: 0 (if 1 maps to 0) or small
        # Freshness: 0 (>7 days)
        
        # Let's adjust vibe expectation: 1/10 maps to 10/100? or 0? 
        # Spec: "Scale the existing 1-10 score to 0-100." -> 1=10, 10=100.
        expected_vibe = 10 * 0.2 
        
        self.assertAlmostEqual(score_data['total'], expected_vibe) 

    def test_redistribute_missing_commute(self):
        """Test that missing commute redistributes weight to others."""
        property_data = {
            "price": "£1,000 pcm", # Max score (100)
            "commute_time": None, # Missing
            "vibe_score": 10, # Max score (100)
            "published_on": "2023-10-27T10:00:00Z" # Max score (100)
        }
        global_stats = {"min_price": 1000, "max_price": 2000}

        # Weights: Price 0.3, Vibe 0.2, Freshness 0.1. Total valid = 0.6
        # New Weights: 
        # Price = 0.3 / 0.6 = 0.5
        # Vibe = 0.2 / 0.6 = 0.333
        # Freshness = 0.1 / 0.6 = 0.166
        
        # Expected Score:
        # Price: 100 * 0.5 = 50
        # Vibe: 100 * 0.333 = 33.33
        # Freshness: 100 * 0.166 = 16.66
        # Total = 100
        
        with patch('scoring.get_days_since', return_value=0):
            score_data = self.scorer.calculate_score(property_data, global_stats)
            
        self.assertAlmostEqual(score_data['total'], 100.0)
        self.assertIsNone(score_data['breakdown']['commute'])

    def test_missing_price_returns_zero(self):
        """Test that missing price results in 0 score."""
        property_data = {"price": None}
        global_stats = {"min_price": 1000, "max_price": 2000}
        
        score_data = self.scorer.calculate_score(property_data, global_stats)
        self.assertEqual(score_data['total'], 0)

if __name__ == '__main__':
    unittest.main()
