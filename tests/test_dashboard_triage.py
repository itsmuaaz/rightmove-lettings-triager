import unittest
from unittest.mock import MagicMock
from io import BytesIO
import json
from dashboard import DashboardHandler

class TestDashboardHandlerTriage(unittest.TestCase):
    def setUp(self):
        class MockServer:
            pass
        self.mock_server = MockServer()
        self.mock_server.history_manager = MagicMock()

    def _make_handler(self, path='/', method='POST', body=None, headers=None):
        # BaseHTTPRequestHandler __init__ calls methods, so we use __new__ and manual setup
        # or we could mock the socket. Here we use a minimal approach to avoid complex mocks.
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
        
        # Mock send_response and end_headers
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.send_error = MagicMock()
        
        return handler

    def test_post_shortlist(self):
        """Test POST /api/history with action: shortlist."""
        data = json.dumps({"id": "prop1", "action": "shortlist"}).encode()
        headers = {'Content-Length': str(len(data))}
        
        handler = self._make_handler(path='/api/history', method='POST', body=data, headers=headers)
        handler.do_POST()
        
        # Verify mark_shortlisted was called
        self.mock_server.history_manager.mark_shortlisted.assert_called_with("prop1")
        handler.send_response.assert_called_with(200)

if __name__ == '__main__':
    unittest.main()
