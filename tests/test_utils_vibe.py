import unittest
from utils import extract_postcode_district, extract_location_for_vibe, get_sort_key

class TestUtilsVibe(unittest.TestCase):
    def test_extract_postcode_district(self):
        self.assertEqual(extract_postcode_district("123 High St, SW14 7AB"), "SW14")
        self.assertEqual(extract_postcode_district("Flat 1, E1 6AN"), "E1")
        self.assertEqual(extract_postcode_district("N1C 4AG"), "N1C")
        self.assertEqual(extract_postcode_district("No Postcode Here"), None)
        self.assertEqual(extract_postcode_district(""), None)
        self.assertEqual(extract_postcode_district(None), None)

    def test_extract_location_for_vibe(self):
        # Postcode present
        self.assertEqual(extract_location_for_vibe("123 High St, SW14 7AB"), "SW14")
        
        # Postcode missing, return cleaned address
        self.assertEqual(extract_location_for_vibe("Mazenod Avenue, West Hampstead"), "Mazenod Avenue, West Hampstead")
        
        # Empty/None
        self.assertEqual(extract_location_for_vibe(""), None)
        self.assertEqual(extract_location_for_vibe(None), None)
        self.assertEqual(extract_location_for_vibe("   "), None)

    def test_get_sort_key(self):
        # Both present
        self.assertEqual(get_sort_key({'commute_time': 30, 'commute_cycling': 40}), 30)
        self.assertEqual(get_sort_key({'commute_time': 50, 'commute_cycling': 40}), 40)
        
        # One present
        self.assertEqual(get_sort_key({'commute_time': 30, 'commute_cycling': None}), 30)
        self.assertEqual(get_sort_key({'commute_time': None, 'commute_cycling': 40}), 40)
        
        # None present
        self.assertEqual(get_sort_key({'commute_time': None, 'commute_cycling': None}), float('inf'))

if __name__ == '__main__':
    unittest.main()
