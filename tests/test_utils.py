import unittest
from utils import haversine

class TestUtils(unittest.TestCase):
    def test_haversine(self):
        # Distance between London (51.5074, -0.1278) and Paris (48.8566, 2.3522)
        # is approx 213 miles
        dist = haversine(51.5074, -0.1278, 48.8566, 2.3522)
        self.assertAlmostEqual(dist, 213.3, delta=1.0)

    def test_haversine_same_point(self):
        dist = haversine(51.5, -0.1, 51.5, -0.1)
        self.assertEqual(dist, 0.0)

if __name__ == "__main__":
    unittest.main()
