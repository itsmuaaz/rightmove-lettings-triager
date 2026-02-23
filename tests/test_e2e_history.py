import unittest
import os
import json
import tempfile
import shutil
import threading
import time
from http.server import HTTPServer
from threading import Thread
import urllib.request
from dashboard import DashboardHandler
from history_manager import HistoryManager

class TestEndToEndHistory(unittest.TestCase):
    def setUp(self):
        # Temp dirs
        self.test_dir = tempfile.mkdtemp()
        self.history_file = os.path.join(self.test_dir, "history.json")
        self.notes_file = os.path.join(self.test_dir, "notes.json")
        
        # Setup Managers
        self.history_manager = HistoryManager(self.history_file)
        # We need to mock NoteManager or just let it use default (which we should avoid in test)
        # Assuming NoteManager is robust or we mock it.
        # Let's mock NoteManager for simplicity
        self.note_manager = MagicMock()
        self.note_manager.get_note.return_value = ""

        # Setup Server
        self.port = 8999
        self.server = HTTPServer(('127.0.0.1', self.port), DashboardHandler)
        self.server.history_manager = self.history_manager
        self.server.note_manager = self.note_manager
        self.server.reporter = MagicMock() # Not needed for API tests
        self.server.properties = [] 

        # Start Server in Thread
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(0.5) # Wait for startup

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        shutil.rmtree(self.test_dir)

    def test_api_updates_history_file(self):
        """Verify that hitting the API updates the local JSON file."""
        url = f"http://127.0.0.1:{self.port}/api/history"
        
        # Action: Mark View
        data = json.dumps({"id": "prop123", "action": "view"}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)

        # Verify File Update
        # Reload manager to check file content
        new_manager = HistoryManager(self.history_file)
        status = new_manager.get_status("prop123")
        self.assertEqual(status['status'], 'viewed')

    def test_api_dismiss_action(self):
        """Verify dismiss action."""
        url = f"http://127.0.0.1:{self.port}/api/history"
        data = json.dumps({"id": "prop456", "action": "dismiss"}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            
        new_manager = HistoryManager(self.history_file)
        status = new_manager.get_status("prop456")
        self.assertEqual(status['status'], 'dismissed')

from unittest.mock import MagicMock
