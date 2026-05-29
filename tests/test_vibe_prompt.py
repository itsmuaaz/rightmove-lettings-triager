import unittest
from vibe_client import VibeClient

class TestVibePromptRefinement(unittest.TestCase):
    def test_prompt_contains_new_criteria(self):
        """Test that the prompt includes the new comprehensive criteria."""
        client = VibeClient()
        client.config = {"api": {"gemini": {"custom_criteria": "- Safety\n- demographic\n- gentrification\n- atmosphere"}}}
        
        locations = ["SW1A"]
        
        if hasattr(client, '_generate_prompt'):
            prompt = client._generate_prompt(locations)
            self.assertIn("Safety", prompt)
            self.assertIn("demographic", prompt)
            self.assertIn("gentrification", prompt)
            self.assertIn("atmosphere", prompt)
        else:
            self.fail("VibeClient needs refactoring to expose _generate_prompt")

if __name__ == '__main__':
    unittest.main()
