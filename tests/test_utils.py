import unittest
from utils import haversine, generate_google_maps_url, generate_tfl_url

class TestUtils(unittest.TestCase):
    def test_haversine(self):
        # Distance between London (51.5074, -0.1278) and Paris (48.8566, 2.3522)
        # is approx 213 miles
        dist = haversine(51.5074, -0.1278, 48.8566, 2.3522)
        self.assertAlmostEqual(dist, 213.3, delta=1.0)

    def test_haversine_same_point(self):
        dist = haversine(51.5, -0.1, 51.5, -0.1)
        self.assertEqual(dist, 0.0)

    def test_generate_google_maps_url(self):
        origin = "10 Downing St, London"
        expected_part = "origin=10+Downing+St%2C+London"
        expected_dest = "destination=6+Pancras+Square%2C+N1C+4AG"
        expected_mode = "travelmode=transit"
        
        url = generate_google_maps_url(origin)
        
        self.assertIn("https://www.google.com/maps/dir/?api=1", url)
        self.assertIn(expected_part, url)
        self.assertIn(expected_dest, url)
        self.assertIn(expected_mode, url)

    def test_generate_tfl_url(self):
        origin_address = "10 Downing St, London"
        origin_coords = (51.5034, -0.1276)
        
        url = generate_tfl_url(origin_address, origin_coords)
        
        self.assertIn("https://tfl.gov.uk/plan-a-journey/results", url)
        self.assertIn("InputFrom=10+Downing+St%2C+London", url)
        self.assertIn("FromId=51.5034%2C-0.1276", url)
        self.assertIn("InputTo=6+Pancras+Square%2C+N1C+4AG", url)
        self.assertIn("ToId=51.5349%2C-0.1238", url)

    def test_generate_tfl_url_no_coords(self):
        origin_address = "10 Downing St, London"
        
        url = generate_tfl_url(origin_address, None)
        
        self.assertIn("InputFrom=10+Downing+St%2C+London", url)
        self.assertNotIn("FromId=", url)

if __name__ == "__main__":
    unittest.main()
