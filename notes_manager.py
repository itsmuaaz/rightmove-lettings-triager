import json
import os
import shutil
import tempfile
from datetime import datetime

class NoteManager:
    """Manages persistent storage of property notes using a JSON file."""

    def __init__(self, filepath='notes.json'):
        self.filepath = filepath
        self._cache = self._load_notes()

    def _load_notes(self):
        """Loads notes from the file, returning an empty dict if not found."""
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def get_all_notes(self):
        """Returns a dictionary of all notes."""
        return self._cache

    def get_note(self, property_id):
        """Returns the note content for a property ID, or None."""
        entry = self._cache.get(str(property_id))
        return entry.get('content') if entry else None

    def save_note(self, property_id, content):
        """Saves a note for a property, updating the timestamp."""
        property_id = str(property_id)
        
        self._cache[property_id] = {
            'content': content,
            'updated_at': datetime.now().isoformat()
        }
        self._persist_to_disk()

    def _persist_to_disk(self):
        """Writes the current cache to disk atomically."""
        # Write to a temp file first
        dir_name = os.path.dirname(self.filepath) or '.'
        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=dir_name) as tmp:
            json.dump(self._cache, tmp, indent=2)
            temp_name = tmp.name
        
        # Atomic rename
        shutil.move(temp_name, self.filepath)
