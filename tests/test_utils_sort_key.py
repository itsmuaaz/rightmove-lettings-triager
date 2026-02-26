import unittest
from utils import create_sort_key

class TestUtilsSortKey(unittest.TestCase):

    def setUp(self):
        self.prop_base = {
            'id': '123',
            'price': 2000.0,
            'smart_score': 85.0,
            'vibe_score': 7.5,
            'added_on': '2023-10-25T10:00:00Z',
            'commute_time': 45,
            'commute_cycling': 30
        }

    def test_sort_by_price(self):
        key = create_sort_key(self.prop_base, sort_by='price')
        self.assertEqual(key, 2000.0)

    def test_sort_by_smart_score(self):
        key = create_sort_key(self.prop_base, sort_by='smart_score')
        self.assertEqual(key, 85.0)

    def test_sort_by_vibe(self):
        # Raw data has nested vibe dict
        prop = {'id': '123', 'vibe': {'score': 7.5}}
        key = create_sort_key(prop, sort_by='vibe_score')
        self.assertEqual(key, 7.5)
        
        # Fallback for flat structure (if enriched)
        prop_flat = {'id': '123', 'vibe_score': 8.0}
        key_flat = create_sort_key(prop_flat, sort_by='vibe_score')
        self.assertEqual(key_flat, 8.0)

    def test_sort_by_added_on(self):
        key = create_sort_key(self.prop_base, sort_by='added_on')
        self.assertEqual(key, '2023-10-25T10:00:00Z')

    def test_sort_by_commute_min(self):
        key = create_sort_key(self.prop_base, sort_by='commute', mode='min')
        self.assertEqual(key, 30) # min(45, 30)

    def test_sort_by_commute_transport(self):
        key = create_sort_key(self.prop_base, sort_by='commute', mode='transport')
        self.assertEqual(key, 45)

    def test_sort_by_commute_cycling(self):
        key = create_sort_key(self.prop_base, sort_by='commute', mode='cycling')
        self.assertEqual(key, 30)

    def test_sort_by_commute_default_mode(self):
        # Should default to 'min'
        key = create_sort_key(self.prop_base, sort_by='commute')
        self.assertEqual(key, 30)

    def test_missing_values(self):
        prop = {'id': '123'}
        
        # Test default fallback for numeric fields (infinity ensures they go to end in ASC sort)
        self.assertEqual(create_sort_key(prop, 'price'), float('inf'))
        # For smart_score, usually we want high scores first, but sort key is raw value.
        # Dashboard handles ASC/DESC. If ASC sort (low->high), None should be last?
        # Actually standard python sort is stable. Let's stick to simple extraction first.
        # But wait, python 3 cannot compare float and None. So we MUST return a sentinel.
        # Spec says: "properties with unknown price or commute should appear at the end".
        # If sorting ASC (Low->High), end means HIGH value (inf).
        # If sorting DESC (High->Low), end means LOW value (-inf).
        # However, `create_sort_key` usually just extracts the value. 
        # The caller (DashboardHandler) might handle the direction.
        # Let's assume `create_sort_key` returns a comparable value.
        
        # For Price (Low is good): Missing -> Inf (so it's "high" price)
        self.assertEqual(create_sort_key(prop, 'price'), float('inf'))

        # For Commute (Low is good): Missing -> Inf
        self.assertEqual(create_sort_key(prop, 'commute'), float('inf'))

        # For Score (High is good): Missing -> -1 (so it's "low" score)
        # Assuming scores are positive.
        self.assertEqual(create_sort_key(prop, 'smart_score'), -1.0)
        
        # For Vibe (High is good): Missing -> -1
        self.assertEqual(create_sort_key(prop, 'vibe_score'), -1.0)

        # For Added On (New is good): Missing -> empty string or old date?
        # String comparison: empty string is "small". 
        # If sorting DESC (Newest first), "small" goes to end. Correct.
        self.assertEqual(create_sort_key(prop, 'added_on'), '')

if __name__ == "__main__":
    unittest.main()
