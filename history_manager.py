"""Module for managing the history of property interactions (viewed, shortlisted, dismissed)."""

import json
import os
import time
import shutil
import tempfile
from datetime import datetime
from typing import Dict, Any, Optional

class HistoryManager:
    """Manages the history state of properties (new/viewed/dismissed)."""

    def __init__(self, history_file: str = "history.json"):
        """Initializes the manager with a file path."""
        self.history_file = history_file
        self.history: Dict[str, Any] = {}
        self._load_history()

    def _load_history(self) -> None:
        """Loads history from the JSON file."""
        if not os.path.exists(self.history_file):
            self.history = {}
            return

        try:
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        except (json.JSONDecodeError, IOError):
            # If corrupted or empty, start fresh (or could raise error)
            self.history = {}

    def _save_history(self) -> None:
        """Saves history to the JSON file atomically."""
        # Atomic write: write to temp file, then rename
        dir_name = os.path.dirname(self.history_file) or "."
        with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False) as tf:
            json.dump(self.history, tf, indent=2)
            temp_name = tf.name
        
        try:
            os.replace(temp_name, self.history_file)
        except OSError:
            # Fallback for systems where replace might fail across devices
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            os.rename(temp_name, self.history_file)

    def get_status(self, property_id: str) -> Optional[Dict[str, Any]]:
        """Returns the history entry for a property ID."""
        return self.history.get(property_id)

    def mark_seen(self, property_id: str) -> None:
        """Marks a property as viewed.
        
        Args:
            property_id: The unique ID of the property.
        """
        entry = self.history.get(property_id, {})
        if not entry:
            entry = {
                "first_seen": datetime.now().isoformat(),
                "status": "viewed"
            }
        
        entry['last_viewed'] = datetime.now().isoformat()
        
        # Only set to 'viewed' if not already 'shortlisted' or 'dismissed'
        if entry.get('status') not in ['shortlisted', 'dismissed']:
            entry['status'] = 'viewed'
            
        self.history[property_id] = entry
        self._save_history()

    def mark_shortlisted(self, property_id: str) -> None:
        """Marks a property as shortlisted.
        
        Args:
            property_id: The unique ID of the property.
        """
        entry = self.history.get(property_id, {})
        if not entry:
            entry = {
                "first_seen": datetime.now().isoformat()
            }
        
        entry['status'] = 'shortlisted'
        self.history[property_id] = entry
        self._save_history()

    def unshortlist(self, property_id: str) -> None:
        """Reverts a property from shortlisted to viewed.
        
        Args:
            property_id: The unique ID of the property.
        """
        entry = self.history.get(property_id, {})
        if entry:
            entry['status'] = 'viewed'
            self.history[property_id] = entry
            self._save_history()

    def mark_dismissed(self, property_id: str) -> None:
        """Marks a property as dismissed.
        
        Args:
            property_id: The unique ID of the property.
        """
        entry = self.history.get(property_id, {})
        if not entry:
            entry = {
                "first_seen": datetime.now().isoformat(),
                "status": "dismissed"
            }
        
        entry['status'] = 'dismissed'
        self.history[property_id] = entry
        self._save_history()

    def initialize_properties(self, properties: list) -> None:
        """Ensures all properties in the list have a history entry.
        
        Args:
            properties: A list of property dictionaries.
        """
        changed = False
        for prop in properties:
            pid = prop.get('id')
            if not pid:
                continue
            
            agency_name = prop.get('agency_name')
            agency_phone = prop.get('agency_phone')
                
            if pid not in self.history:
                self.history[pid] = {
                    "first_seen": datetime.now().isoformat(),
                    "status": "new",
                    "agency_name": agency_name,
                    "agency_phone": agency_phone
                }
                changed = True
            else:
                # Update existing entry if agency info is missing or changed
                entry = self.history[pid]
                updated = False
                if agency_name and entry.get('agency_name') != agency_name:
                    entry['agency_name'] = agency_name
                    updated = True
                if agency_phone and entry.get('agency_phone') != agency_phone:
                    entry['agency_phone'] = agency_phone
                    updated = True
                
                if updated:
                    self.history[pid] = entry
                    changed = True
        
        if changed:
            self._save_history()
