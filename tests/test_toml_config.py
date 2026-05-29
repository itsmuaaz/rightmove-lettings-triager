import unittest
from unittest.mock import patch, mock_open, MagicMock
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
    @patch.dict(os.environ, {"TFL_APP_ID": "env_id", "TFL_APP_KEY": "env_key"})
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

    @patch('os.path.exists', return_value=True)
    def test_save_config_updates_toml(self, mock_exists):
        initial_toml = """
[search]
work_latitude = 51.5

[scoring.weights]
# Price is very important
price = 0.3
commute = 0.3
vibe = 0.3
freshness = 0.1
"""
        
        manager = ConfigManager("test_save.toml", self.defaults)
        
        new_weights = {
            "price": 50,
            "commute": 50,
            "vibe": 0,
            "freshness": 0
        }

        # Python's mock_open has a quirk with readlines when iterating. 
        # Best to just mock the file operations directly for this specific test case.
        file_writes = []
        def mock_file_open(file, mode='r', **kwargs):
            m = MagicMock()
            if mode == 'r':
                m.__enter__.return_value.readlines.return_value = [line + '\n' for line in initial_toml.split('\n')]
            elif mode == 'w':
                m.__enter__.return_value.writelines.side_effect = lambda lines: file_writes.extend(lines)
            return m

        with patch('builtins.open', side_effect=mock_file_open):
            manager.save_config(new_weights)

        written_content = "".join(file_writes)

        self.assertIn("price = 0.5", written_content)
        self.assertIn("commute = 0.5", written_content)
        self.assertIn("vibe = 0.0", written_content)
        self.assertIn("freshness = 0.0", written_content)
        self.assertIn("[search]", written_content)
        self.assertIn("work_latitude = 51.5", written_content)
        self.assertIn("# Price is very important", written_content)

if __name__ == '__main__':
    unittest.main()
