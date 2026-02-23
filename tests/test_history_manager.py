import unittest
import os
import shutil
import json
import tempfile
from datetime import datetime
from history_manager import HistoryManager

class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for history
        self.test_dir = tempfile.mkdtemp()
        self.history_file = os.path.join(self.test_dir, "test_history.json")
        self.manager = HistoryManager(self.history_file)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_init_creates_empty_history(self):
        """Test that initialization handles a missing file gracefully."""
        self.assertFalse(os.path.exists(self.history_file))
        # Ensure loading doesn't crash
        status = self.manager.get_status("some_id")
        self.assertIsNone(status)

    def test_save_and_load_history(self):
        """Test persistence."""
        self.manager.mark_seen("prop1")
        
        # New instance to verify persistence
        new_manager = HistoryManager(self.history_file)
        status = new_manager.get_status("prop1")
        self.assertEqual(status['status'], 'viewed')
        self.assertIn('first_seen', status)
        self.assertIn('last_viewed', status)

    def test_mark_seen(self):
        """Test marking a property as seen (viewed)."""
        # Scenario 1: New property
        self.manager.mark_seen("prop1")
        status = self.manager.get_status("prop1")
        self.assertEqual(status['status'], 'viewed')
        self.assertIsNotNone(status.get('last_viewed'))

        # Scenario 2: Existing property (should update last_viewed)
        first_view = status['last_viewed']
        # Mock time passing (in a real scenario we'd mock datetime.now)
        self.manager.mark_seen("prop1") 
        new_status = self.manager.get_status("prop1")
        self.assertEqual(new_status['status'], 'viewed')
        
    def test_mark_dismissed(self):
        """Test marking a property as dismissed."""
        self.manager.mark_dismissed("prop2")
        status = self.manager.get_status("prop2")
        self.assertEqual(status['status'], 'dismissed')

    def test_initialize_new_properties(self):
        """Test initializing a list of properties as 'new' if not present."""
        properties = [{"id": "p1"}, {"id": "p2"}]
        # Pre-populate p1 as dismissed
        self.manager.mark_dismissed("p1")
        
        self.manager.initialize_properties(properties)
        
        # p1 should remain dismissed
        s1 = self.manager.get_status("p1")
        self.assertEqual(s1['status'], 'dismissed')
        
        # p2 should be new
        s2 = self.manager.get_status("p2")
        self.assertEqual(s2['status'], 'new')
        self.assertIsNotNone(s2.get('first_seen'))

    def test_atomic_write(self):
        """Verify that writes are atomic (implied by not crashing/corrupting)."""
        # This is hard to test deterministically without mocking filesystem locks/race conditions,
        # but we can ensure the basic mechanism works.
        self.manager.mark_seen("p1")
        self.assertTrue(os.path.exists(self.history_file))

if __name__ == '__main__':
    unittest.main()
