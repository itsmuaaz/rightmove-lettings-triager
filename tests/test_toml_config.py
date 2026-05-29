import unittest
from unittest.mock import patch, mock_open
import os
import tomllib
from config_manager import ConfigManager

class TestTomlConfigManager(unittest.TestCase):
    def setUp(self):
        self.defaults = {
            "search": {
                "work_latitude": 51.5349,
                "work_longitude": -0.1238
            },
            "scoring": {
                "weights": {
                    "price": 0.3,
                    "commute": 0.3,
                    "vibe": 0.3,
                    "freshness": 0.1
                }
            }
        }

    @patch('os.path.exists')
    @patch('shutil.copyfile')
    def test_load_config_missing_file_copies_template(self, mock_copy, mock_exists):
        # exists.toml doesn't exist, but template DOES exist
        mock_exists.side_effect = lambda path: path == "missing.toml.template"
        manager = ConfigManager("missing.toml", self.defaults)
        
        with patch('builtins.open', side_effect=FileNotFoundError):
            config = manager.load_config()
            
        mock_copy.assert_called_once_with("missing.toml.template", "missing.toml")
        self.assertEqual(config, self.defaults)

    @patch('os.path.exists', return_value=True)
    def test_load_config_merges_toml_with_defaults(self, mock_exists):
        toml_content = b"""
        [search]
        work_latitude = 50.0
        
        [scoring.weights]
        price = 0.5
        """
        manager = ConfigManager("exists.toml", self.defaults)
        
        with patch('builtins.open', mock_open(read_data=toml_content)):
            config = manager.load_config()
            
        # Overridden value
        self.assertEqual(config['search']['work_latitude'], 50.0)
        # Default fallback value
        self.assertEqual(config['search']['work_longitude'], -0.1238)
        # Overridden value in nested dict
        self.assertEqual(config['scoring']['weights']['price'], 0.5)
        # Default fallback in nested dict
        self.assertEqual(config['scoring']['weights']['commute'], 0.3)

    @patch('os.path.exists', return_value=True)
    @patch.dict(os.environ, {"TFL_APP_ID": "env_id", "TFL_APP_KEY": "env_key", "GOOGLE_MAPS_API_KEY": "env_maps"})
    def test_load_config_merges_env_overrides(self, mock_exists):
        toml_content = b"""
        [credentials]
        tfl_app_id = "toml_id"
        tfl_app_key = "toml_key"
        """
        manager = ConfigManager("exists.toml", self.defaults)
        
        with patch('builtins.open', mock_open(read_data=toml_content)):
            config = manager.load_config()
            
        # Env variables should override TOML
        self.assertEqual(config['credentials']['tfl_app_id'], "env_id")
        self.assertEqual(config['credentials']['tfl_app_key'], "env_key")
        self.assertEqual(config['credentials']['google_maps_api_key'], "env_maps")

if __name__ == '__main__':
    unittest.main()
