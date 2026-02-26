import os
import unittest
from unittest.mock import patch
from config import load_config

class TestConfig(unittest.TestCase):
    @patch.dict(os.environ, {"TFL_APP_ID": "test_id", "TFL_APP_KEY": "test_key"})
    def test_load_config_tfl(self):
        config = load_config()
        self.assertEqual(config.get("TFL_APP_ID"), "test_id")
        self.assertEqual(config.get("TFL_APP_KEY"), "test_key")

    @patch.dict(os.environ, {"GOOGLE_MAPS_API_KEY": "google_key"})
    def test_load_config_google(self):
        config = load_config()
        self.assertEqual(config.get("GOOGLE_MAPS_API_KEY"), "google_key")

    def test_load_config_scoring_defaults(self):
        """Test that default scoring configuration is loaded."""
        config = load_config()
        weights = config.get("SCORING_WEIGHTS")
        self.assertIsNotNone(weights)
        self.assertAlmostEqual(sum(weights.values()), 1.0)
        self.assertEqual(config.get("MAX_COMMUTE_MINS"), 60)
        self.assertEqual(config.get("FRESHNESS_DECAY_DAYS"), 7)

if __name__ == "__main__":
    unittest.main()
