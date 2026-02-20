import unittest
import os
import json
import tempfile
import shutil
from notes_manager import NoteManager

class TestNoteManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.notes_file = os.path.join(self.test_dir, 'notes.json')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_notes_empty(self):
        """Test loading when file doesn't exist."""
        manager = NoteManager(self.notes_file)
        self.assertEqual(manager.get_all_notes(), {})

    def test_save_and_load_note(self):
        """Test saving a note and reloading it."""
        manager = NoteManager(self.notes_file)
        manager.save_note('123', 'Test note')
        
        # Reload manager to simulate fresh start
        new_manager = NoteManager(self.notes_file)
        notes = new_manager.get_all_notes()
        self.assertIn('123', notes)
        self.assertEqual(notes['123']['content'], 'Test note')
        self.assertIn('updated_at', notes['123'])

    def test_update_existing_note(self):
        """Test updating a note preserves content."""
        manager = NoteManager(self.notes_file)
        manager.save_note('123', 'Initial content')
        manager.save_note('123', 'Updated content')
        
        notes = manager.get_all_notes()
        self.assertEqual(notes['123']['content'], 'Updated content')

    def test_get_note(self):
        """Test retrieving a single note."""
        manager = NoteManager(self.notes_file)
        manager.save_note('123', 'My note')
        self.assertEqual(manager.get_note('123'), 'My note')
        self.assertIsNone(manager.get_note('999'))

if __name__ == '__main__':
    unittest.main()
