import unittest
from unittest.mock import patch, MagicMock
# We will verify configure_scoring later, assuming it will be in rightmove_search
# For now, we assume it's imported or defined here for the test structure if we were doing strict TDD
# But since rightmove_search is a script, I might need to import it carefully.

try:
    from rightmove_search import configure_scoring
except ImportError:
    configure_scoring = None

class TestInteractivePrompt(unittest.TestCase):
    @patch('builtins.input')
    @patch('rightmove_search.ConfigManager')
    def test_configure_scoring_yes(self, MockConfigManager, mock_input):
        if configure_scoring is None:
            self.fail("configure_scoring not implemented")

        # Setup mocks
        mock_manager = MockConfigManager.return_value
        # Default weights
        mock_manager.load_config.return_value = {"price": 0.3, "commute": 0.3, "vibe": 0.3, "freshness": 0.1}
        
        # Simulate user input: 
        # 1. "y" (Change weights?)
        # 2. "50" (Price)
        # 3. "50" (Commute)
        # 4. "0" (Vibe)
        # 5. "0" (Freshness)
        mock_input.side_effect = ["y", "50", "50", "0", "0"]
        
        configure_scoring()
        
        # Verify save_config called with normalized map
        # configure_scoring handles user input (integers) and passes them to manager.
        # manager.save_config handles normalization. So we expect the raw dict passed to save_config.
        
        expected_raw_weights = {
            "price": 50.0,
            "commute": 50.0,
            "vibe": 0.0,
            "freshness": 0.0
        }
        
        mock_manager.save_config.assert_called_once()
        args, _ = mock_manager.save_config.call_args
        self.assertEqual(args[0], expected_raw_weights)

    @patch('builtins.input')
    @patch('rightmove_search.ConfigManager')
    def test_configure_scoring_no(self, MockConfigManager, mock_input):
        if configure_scoring is None:
            self.fail("configure_scoring not implemented")

        mock_manager = MockConfigManager.return_value
        mock_manager.load_config.return_value = {"price": 0.3, "commute": 0.3, "vibe": 0.3, "freshness": 0.1}
        
        # Simulate user input: "n"
        mock_input.side_effect = ["n"]
        
        configure_scoring()
        
        mock_manager.save_config.assert_not_called()

if __name__ == '__main__':
    unittest.main()
