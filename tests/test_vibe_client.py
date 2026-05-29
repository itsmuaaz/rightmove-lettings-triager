import unittest
from unittest.mock import patch, MagicMock
import subprocess
import json
import os
from vibe_client import VibeClient

class TestVibeClient(unittest.TestCase):
    def setUp(self):
        self.cache_file = ".test_vibe_cache.json"
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        self.client = VibeClient(cache_file=self.cache_file)

    def tearDown(self):
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)

    @patch('subprocess.run')
    def test_get_vibe_success(self, mock_run):
        # Mock successful subprocess response
        mock_response = MagicMock()
        mock_response.stdout = json.dumps({
            "SW14": {
                "score": 8,
                "summary": "Nice place",
                "safety": "High",
                "keywords": ["Green", "Quiet", "Safe"]
            }
        })
        mock_response.returncode = 0
        mock_run.return_value = mock_response

        result = self.client.get_vibes(["SW14"])
        
        self.assertIn("SW14", result)
        self.assertEqual(result["SW14"]["score"], 8)
        self.assertEqual(result["SW14"]["summary"], "Nice place")
        
        # Verify the command was called correctly
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args[0], "gemini")
        self.assertEqual(args[1], "--skip-trust")
        self.assertEqual(args[2], "--prompt")
        self.assertIn("SW14", args[3])

    @patch('subprocess.run')
    def test_get_vibe_invalid_json(self, mock_run):
        # Mock invalid JSON response
        mock_response = MagicMock()
        mock_response.stdout = "This is not JSON"
        mock_response.returncode = 0
        mock_run.return_value = mock_response

        result = self.client.get_vibes(["SW14"])
        
        self.assertEqual(result, {})

    @patch('subprocess.run')
    def test_get_vibe_command_failure(self, mock_run):
        # Mock subprocess error
        mock_run.side_effect = subprocess.CalledProcessError(1, ["gemini", "--skip-trust", "--prompt", "dummy"])

        result = self.client.get_vibes(["SW14"])
        
        self.assertEqual(result, {})
        
    @patch('subprocess.run')
    def test_get_vibe_markdown_json(self, mock_run):
        # Mock response wrapped in markdown code block
        mock_response = MagicMock()
        mock_response.stdout = """```json
{"SW14": {"score": 8}}
```"""
        mock_response.returncode = 0
        mock_run.return_value = mock_response

        result = self.client.get_vibes(["SW14"])
        
        self.assertIn("SW14", result)
        self.assertEqual(result["SW14"]["score"], 8)

    def test_load_cache_valid(self):
        """Test loading a valid cache file."""
        with open(self.cache_file, 'w') as f:
            json.dump({"TEST": {"score": 1}}, f)
        
        client = VibeClient(cache_file=self.cache_file)
        self.assertEqual(client.cache, {"TEST": {"score": 1}})

    def test_load_cache_corrupt(self):
        """Test loading a corrupt cache file returns empty dict."""
        with open(self.cache_file, 'w') as f:
            f.write("invalid json")
            
        client = VibeClient(cache_file=self.cache_file)
        self.assertEqual(client.cache, {})

    def test_save_cache(self):
        """Test saving cache works."""
        self.client.cache = {"TEST": {"score": 5}}
        self.client._save_cache()
        
        with open(self.cache_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data, {"TEST": {"score": 5}})


if __name__ == '__main__':
    unittest.main()
