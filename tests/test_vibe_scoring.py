import unittest
from vibe_client import VibeClient

class TestVibeScoring(unittest.TestCase):
    def test_prompt_enforces_stricter_scoring(self):
        """Test that the prompt includes instructions to guide scoring distribution."""
        client = VibeClient()
        locations = ["SW1A"]
        if hasattr(client, '_generate_prompt'):
            prompt = client._generate_prompt(locations)
            self.assertIn("avoid grade inflation", prompt.lower())
        else:
            self.fail("VibeClient needs refactoring to expose _generate_prompt")

if __name__ == '__main__':
    unittest.main()
