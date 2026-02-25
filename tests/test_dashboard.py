import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
import json
from dashboard import DashboardHandler

class TestDashboardHandler(unittest.TestCase):
    def setUp(self):
        class MockServer:
            pass
        self.mock_server = MockServer()
        self.mock_server.note_manager = MagicMock()
        self.mock_server.html_content = "<html>Fallback</html>"
        self.mock_server.properties = [] # Add this to test fallback properly or dynamic path

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

    def test_get_root_fallback(self):
        """Test GET / returns fallback HTML when reporter/properties not set."""
        # Unset properties or reporter to trigger fallback
        if hasattr(self.mock_server, 'properties'):
             del self.mock_server.properties
        
        handler = self._make_handler(path='/')
        handler.do_GET()
        
        response = handler.wfile.getvalue().decode()
        self.assertIn("HTTP/1.1 200 OK", response)
        self.assertIn("<html>Fallback</html>", response)

    def test_get_root_dynamic(self):
        """Test GET / returns generated HTML when reporter is present."""
        self.mock_server.properties = [{'id': '1', 'note': 'old'}]
        self.mock_server.reporter = MagicMock()
        self.mock_server.reporter.generate_report.return_value = "<html>Generated</html>"
        self.mock_server.note_manager.get_note.return_value = "new note"
        
        # history manager is optional in do_GET logic but let's mock it
        self.mock_server.history_manager = MagicMock()
        self.mock_server.history_manager.get_status.return_value = 'seen'

        handler = self._make_handler(path='/')
        handler.do_GET()
        
        response = handler.wfile.getvalue().decode()
        self.assertIn("HTTP/1.1 200 OK", response)
        self.assertIn("<html>Generated</html>", response)
        
        # Verify enrichment calls
        self.mock_server.note_manager.get_note.assert_called_with('1')
        self.mock_server.history_manager.get_status.assert_called_with('1')
        self.mock_server.reporter.generate_report.assert_called()

    def test_post_note(self):
        """Test POST /api/notes saves the note."""
        data = json.dumps({"id": "123", "note": "New note"}).encode()
        headers = {'Content-Length': str(len(data))}
        
        handler = self._make_handler(path='/api/notes', method='POST', body=data, headers=headers)
        handler.do_POST()
        
        response = handler.wfile.getvalue().decode()
        self.assertIn("HTTP/1.1 200 OK", response)
        self.mock_server.note_manager.save_note.assert_called_with("123", "New note")

    def test_post_refresh(self):
        """Test POST /api/refresh re-calculates commute data."""
        prop = {
            'id': '123',
            'latitude': 51.5,
            'longitude': -0.1,
            'price': '£1500',
            'commute_time': 30
        }
        self.mock_server.properties = [prop]
        self.mock_server.tfl_client = MagicMock()
        self.mock_server.tfl_client.get_commute_time.return_value = 25
        self.mock_server.tfl_client.get_cycling_time.return_value = 15
        
        data = json.dumps({"id": "123"}).encode()
        headers = {'Content-Length': str(len(data))}
        
        handler = self._make_handler(path='/api/refresh', method='POST', body=data, headers=headers)
        handler.do_POST()
        
        response = handler.wfile.getvalue().decode()
        self.assertIn("HTTP/1.1 200 OK", response)
        
        # Verify property updated
        self.assertEqual(prop['commute_time'], 25)
        self.assertEqual(prop['cycling_time'], 15)
        self.assertIn('commute_updated_at', prop)
        
        # Verify client called with force_refresh=True
        from utils import WORK_COORDS
        self.mock_server.tfl_client.get_commute_time.assert_called_with(
            (51.5, -0.1), WORK_COORDS, force_refresh=True
        )
        self.mock_server.tfl_client.get_cycling_time.assert_called_with(
            (51.5, -0.1), WORK_COORDS, force_refresh=True
        )

if __name__ == '__main__':
    unittest.main()
