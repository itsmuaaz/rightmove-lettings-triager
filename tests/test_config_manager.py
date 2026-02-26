import unittest
import json
import os
from config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.test_config_file = ".test_scoring_config.json"
        # Defaults matching the spec (decimals)
        self.defaults = {
            "price": 0.3,
            "commute": 0.3,
            "vibe": 0.3,
            "freshness": 0.1
        }
        self.manager = ConfigManager(config_file=self.test_config_file, defaults=self.defaults)

    def tearDown(self):
        if os.path.exists(self.test_config_file):
            os.remove(self.test_config_file)

    def test_load_defaults_when_file_missing(self):
        config = self.manager.load_config()
        self.assertEqual(config, self.defaults)

    def test_save_and_load_config(self):
        # Save integers (user input simulation)
        # But save_config should probably take the finalized weights?
        # Let's assume save_config takes the raw user dictionary and normalizes it before saving.
        
        user_input = {
            "price": 50,
            "commute": 50,
            "vibe": 0,
            "freshness": 0
        }
        
        # Expected normalized: 0.5, 0.5, 0.0, 0.0
        expected_config = {
            "price": 0.5,
            "commute": 0.5,
            "vibe": 0.0,
            "freshness": 0.0
        }
        
        self.manager.save_config(user_input)
        loaded_config = self.manager.load_config()
        
        for k, v in expected_config.items():
            self.assertAlmostEqual(loaded_config[k], v)

    def test_normalize_weights(self):
        raw_weights = {
            "price": 50,
            "commute": 50,
            "vibe": 50,
            "freshness": 50
        }
        # Total 200. Each is 50/200 = 0.25
        normalized = self.manager.normalize_weights(raw_weights)
        self.assertAlmostEqual(sum(normalized.values()), 1.0)
        self.assertAlmostEqual(normalized["price"], 0.25)

    def test_normalize_weights_zero_sum(self):
        raw_weights = {
            "price": 0,
            "commute": 0,
            "vibe": 0,
            "freshness": 0
        }
        # Should fallback to defaults if sum is 0
        normalized = self.manager.normalize_weights(raw_weights)
        self.assertEqual(normalized, self.defaults)

if __name__ == "__main__":
    unittest.main()
