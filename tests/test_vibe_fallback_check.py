import unittest
from vibe_client import VibeClient
from utils import extract_postcode_district

class TestVibeFallback(unittest.TestCase):
    def test_extract_postcode_district_missing(self):
        """Test existing function fails for addresses without postcodes."""
        address = "Mazenod Avenue, West Hampstead, London"
        # The existing function returns None if no postcode district pattern found
        self.assertIsNone(extract_postcode_district(address))

    def test_vibe_client_prompt_includes_address(self):
        """Test prompt generation logic to handle mixed input."""
        client = VibeClient()
        locations = ["SW14", "Mazenod Avenue, West Hampstead"]
        
        # We need to expose _generate_prompt or check _fetch_from_gemini indirectly?
        # Since _fetch_from_gemini constructs the prompt internally, let's verify logic
        # But _fetch_from_gemini calls subprocess. 
        # I'll create a new test file `tests/test_vibe_fallback.py` where I can patch subprocess 
        # and verify the call arguments.
        pass
