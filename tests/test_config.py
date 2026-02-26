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

    @patch('config.ConfigManager')
    def test_load_config_uses_config_manager(self, MockConfigManager):
        # Mock instance
        mock_instance = MockConfigManager.return_value
        expected_weights = {"price": 0.5, "commute": 0.5, "vibe": 0.0, "freshness": 0.0}
        mock_instance.load_config.return_value = expected_weights
        
        config = load_config()
        self.assertEqual(config["SCORING_WEIGHTS"], expected_weights)
        # Ensure it was initialized with correct file
        MockConfigManager.assert_called()
        args, kwargs = MockConfigManager.call_args
        self.assertIn('.scoring_config.json', kwargs.get('config_file', args[0] if args else ''))

if __name__ == "__main__":
    unittest.main()
