import unittest
from reporter import Reporter

class TestReporterVibe(unittest.TestCase):
    def test_enrich_property_with_vibe(self):
        reporter = Reporter()
        p = {
            'id': '1',
            'address': 'Test Address',
            'vibe': {
                'score': 8,
                'summary': 'Nice place',
                'safety': 'High'
            }
        }
        
        enriched = reporter._enrich_property(p)
        
        # Verify keys are present
        self.assertIn('vibe', enriched)
        self.assertEqual(enriched['vibe_score'], 8)
        self.assertEqual(enriched['vibe_summary'], 'Nice place')
        self.assertEqual(enriched['vibe_color_class'], 'text-green-600')  # Check color mapping

    def test_enrich_property_without_vibe(self):
        reporter = Reporter()
        p = {
            'id': '1',
            'address': 'Test Address'
        }
        
        enriched = reporter._enrich_property(p)
        
        # Verify fallback behavior
        self.assertIn('vibe_score', enriched)
        self.assertEqual(enriched['vibe_score'], 'N/A')
        self.assertEqual(enriched['vibe_color_class'], 'text-gray-400')

if __name__ == '__main__':
    unittest.main()
