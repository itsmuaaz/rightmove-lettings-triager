import unittest
import os
import shutil
import tempfile
from history_manager import HistoryManager

class TestHistoryManagerTriage(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.history_file = os.path.join(self.test_dir, "test_history.json")
        self.manager = HistoryManager(self.history_file)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_mark_shortlisted_new_property(self):
        """Test marking a completely new property as shortlisted."""
        self.manager.mark_shortlisted("prop1")
        status = self.manager.get_status("prop1")
        self.assertIsNotNone(status)
        self.assertEqual(status['status'], 'shortlisted')
        self.assertIn('first_seen', status)

    def test_mark_shortlisted_existing_property(self):
        """Test transitioning from viewed to shortlisted."""
        self.manager.mark_seen("prop1")
        self.manager.mark_shortlisted("prop1")
        status = self.manager.get_status("prop1")
        self.assertEqual(status['status'], 'shortlisted')

    def test_mark_seen_respects_shortlisted(self):
        """Test that mark_seen does not downgrade a shortlisted property back to viewed."""
        self.manager.mark_shortlisted("prop1")
        # Now mark as seen (e.g., user clicks link)
        self.manager.mark_seen("prop1")
        status = self.manager.get_status("prop1")
        # Should remain shortlisted
        self.assertEqual(status['status'], 'shortlisted')
        self.assertIn('last_viewed', status)

    def test_mark_dismissed_overwrites_shortlisted(self):
        """Test that dismissing a shortlisted property works (user changed mind)."""
        self.manager.mark_shortlisted("prop1")
        self.manager.mark_dismissed("prop1")
        status = self.manager.get_status("prop1")
        self.assertEqual(status['status'], 'dismissed')

if __name__ == '__main__':
    unittest.main()
