import unittest
from search_state import SearchState

class TestSearchState(unittest.TestCase):
    def test_initialization(self):
        state = SearchState()
        self.assertEqual(state.properties, [])
        self.assertEqual(state.total, 0)
        self.assertEqual(state.processed, 0)
        self.assertEqual(state.status, "initializing")

    def test_update_state(self):
        state = SearchState()
        state.total = 10
        state.processed = 5
        state.status = "processing"
        
        self.assertEqual(state.total, 10)
        self.assertEqual(state.processed, 5)
        self.assertEqual(state.status, "processing")
    
    def test_properties_update(self):
        state = SearchState()
        props = [{'id': 1}, {'id': 2}]
        state.properties = props
        self.assertEqual(len(state.properties), 2)

if __name__ == '__main__':
    unittest.main()
