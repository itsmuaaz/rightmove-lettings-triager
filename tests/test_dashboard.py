import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
import json
from dashboard import DashboardHandler

class TestDashboardHandler(unittest.TestCase):
    def setUp(self):
        self.mock_server = MagicMock()
        self.mock_server.note_manager = MagicMock()
        self.mock_server.html_content = "<html>Test</html>"

    def _make_handler(self, path='/', method='GET', body=None, headers=None):
        handler = DashboardHandler.__new__(DashboardHandler)
        handler.server = self.mock_server
        handler.request = MagicMock()
        handler.client_address = ('127.0.0.1', 8888)
        
        handler.path = path
        handler.command = method
        handler.requestline = f"{method} {path} HTTP/1.1"
        handler.request_version = "HTTP/1.1"
        handler.protocol_version = "HTTP/1.1"
        
        # Setup input/output
        if body:
            handler.rfile = BytesIO(body)
        else:
            handler.rfile = BytesIO()
            
        handler.wfile = BytesIO()
        
        # Setup headers
        handler.headers = headers or {}
        
        return handler

    def test_get_root(self):
        """Test GET / returns the HTML content."""
        handler = self._make_handler(path='/')
        handler.do_GET()
        
        response = handler.wfile.getvalue().decode()
        self.assertIn("HTTP/1.1 200 OK", response)
        self.assertIn("<html>Test</html>", response)

    def test_post_note(self):
        """Test POST /api/notes saves the note."""
        data = json.dumps({"id": "123", "note": "New note"}).encode()
        headers = {'Content-Length': str(len(data))}
        
        handler = self._make_handler(path='/api/notes', method='POST', body=data, headers=headers)
        handler.do_POST()
        
        response = handler.wfile.getvalue().decode()
        self.assertIn("HTTP/1.1 200 OK", response)
        self.mock_server.note_manager.save_note.assert_called_with("123", "New note")

if __name__ == '__main__':
    unittest.main()
