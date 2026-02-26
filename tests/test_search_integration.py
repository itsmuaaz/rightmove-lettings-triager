import unittest
from unittest.mock import MagicMock, patch
# We will need to import post_process_properties after we implement it.
# For now, we assume it will be in rightmove_search
try:
    from rightmove_search import post_process_properties
except ImportError:
    post_process_properties = None

class TestSearchIntegration(unittest.TestCase):
    def test_post_process_properties_scoring(self):
        if post_process_properties is None:
            self.fail("post_process_properties not implemented")

        # Mock properties
        properties = [
            {
                "id": "1",
                "price": "£1,000 pcm",
                "commute_time": 20,
                "vibe": {"score": 8},
                "published_on": "2023-10-27T10:00:00Z" # 0 days
            },
            {
                "id": "2",
                "price": "£2,000 pcm",
                "commute_time": 60,
                "vibe": {"score": 2},
                "published_on": "2023-10-20T10:00:00Z" # 7 days
            }
        ]

        # Mock get_days_since to return 0 and 7 respectively
        with patch('scoring.get_days_since', side_effect=[0, 7]):
            processed = post_process_properties(properties)

        # Check if scores are added
        self.assertIn('smart_score', processed[0])
        self.assertIn('score_breakdown', processed[0])
        
        # Prop 1 should have high score
        # Price: Min -> 100
        # Commute: 20 -> 100
        # Vibe: 8 -> 80
        # Freshness: 0 -> 100
        # Weights: 0.3*100 + 0.4*100 + 0.2*80 + 0.1*100 = 30 + 40 + 16 + 10 = 96
        self.assertAlmostEqual(processed[0]['smart_score'], 96.0)

        # Prop 2 should have low score
        # Price: Max -> 0
        # Commute: 60 -> 0
        # Vibe: 2 -> 20
        # Freshness: 7 -> 0
        # Weights: 0.3*0 + 0.4*0 + 0.2*20 + 0.1*0 = 4
        self.assertAlmostEqual(processed[1]['smart_score'], 4.0)

    def test_post_process_sorting(self):
        if post_process_properties is None:
            self.fail("post_process_properties not implemented")

        properties = [
            {"id": "1", "price": "£2,000 pcm", "commute_time": 60, "vibe": {"score": 2}, "published_on": "2023-10-20"},
            {"id": "2", "price": "£1,000 pcm", "commute_time": 20, "vibe": {"score": 8}, "published_on": "2023-10-27"}
        ]
        
        with patch('scoring.get_days_since', side_effect=[7, 0]):
            processed = post_process_properties(properties)
            
        # Should be sorted by score descending (Prop 2 first)
        self.assertEqual(processed[0]['id'], "2")
        self.assertEqual(processed[1]['id'], "1")

if __name__ == '__main__':
    unittest.main()
