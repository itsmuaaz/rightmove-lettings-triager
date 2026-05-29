import unittest
from unittest.mock import patch, MagicMock
import subprocess
from vibe_client import VibeClient
import time

class TestVibeClientRetry(unittest.TestCase):
    def setUp(self):
        self.client = VibeClient(cache_file=".test_retry.json")

    @patch('time.sleep')
    @patch('subprocess.run')
    def test_fetch_from_gemini_retries_on_failure(self, mock_run, mock_sleep):
        # Fail twice, succeed on third try
        error = subprocess.CalledProcessError(1, ["gemini", "--skip-trust", "--prompt", "dummy"])
        success = MagicMock()
        success.stdout = '{"SW14": {"score": 8}}'
        success.returncode = 0
        
        mock_run.side_effect = [error, error, success]

        result = self.client._fetch_from_gemini(["SW14"])

        # Check result
        self.assertEqual(result["SW14"]["score"], 8)
        
        # Check retries
        self.assertEqual(mock_run.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
        # Check backoff times (1, 2)
        mock_sleep.assert_any_call(1)
        mock_sleep.assert_any_call(2)

    @patch('time.sleep')
    @patch('subprocess.run')
    def test_fetch_from_gemini_gives_up_after_max_retries(self, mock_run, mock_sleep):
        # Always fail
        error = subprocess.CalledProcessError(1, ["gemini", "--skip-trust", "--prompt", "dummy"])
        mock_run.side_effect = error
        
        result = self.client._fetch_from_gemini(["SW14"])
        
        self.assertEqual(result, {})
        # Should call initial + 3 retries = 4
        self.assertEqual(mock_run.call_count, 4)

if __name__ == '__main__':
    unittest.main()
