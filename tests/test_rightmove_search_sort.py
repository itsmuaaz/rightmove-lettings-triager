import unittest
from rightmove_search import get_sort_key

class TestRightmoveSort(unittest.TestCase):
    def test_sort_both_commutes(self):
        prop = {'commute_time': 30, 'commute_cycling': 20}
        self.assertEqual(get_sort_key(prop), 20)

    def test_sort_public_only(self):
        prop = {'commute_time': 30, 'commute_cycling': None}
        self.assertEqual(get_sort_key(prop), 30)

    def test_sort_cycling_only(self):
        prop = {'commute_time': None, 'commute_cycling': 25}
        self.assertEqual(get_sort_key(prop), 25)

    def test_sort_no_commute(self):
        prop = {'commute_time': None, 'commute_cycling': None}
        self.assertEqual(get_sort_key(prop), float('inf'))

if __name__ == "__main__":
    unittest.main()
