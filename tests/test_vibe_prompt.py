import unittest
from vibe_client import VibeClient

class TestVibePromptRefinement(unittest.TestCase):
    def test_prompt_contains_new_criteria(self):
        """Test that the prompt includes the new comprehensive criteria."""
        client = VibeClient()
        locations = ["SW1A"]
        # We need to peek at the prompt.
        # Since _fetch_from_gemini generates it inside the function, 
        # I'll extract the prompt generation logic into a helper method `_generate_prompt(locations)`.
        # But first, I'll modify the client to have this method.
        # For this test, I'll assume the client has `_generate_prompt`.
        
        if hasattr(client, '_generate_prompt'):
            prompt = client._generate_prompt(locations)
            self.assertIn("Safety", prompt)
            self.assertIn("Fun", prompt)
            self.assertIn("Amenities", prompt)
            self.assertIn("Cleanliness", prompt)
            self.assertIn("Greenery", prompt)
            self.assertIn("Prestige", prompt)
        else:
            self.fail("VibeClient needs refactoring to expose _generate_prompt")

if __name__ == '__main__':
    unittest.main()
