import unittest
import json
from unittest.mock import MagicMock
from dashboard import DashboardHandler
from history_manager import HistoryManager

class MockRequest:
    def makefile(self, *args, **kwargs):
        return MagicMock()

class MockServer:
    def __init__(self):
        self.history_manager = MagicMock(spec=HistoryManager)
        self.properties = []
        self.reporter = None
        self.note_manager = None

class TestDashboardApi(unittest.TestCase):
    def setUp(self):
        self.server = MockServer()
        
        # Instantiate handler without calling __init__ to avoid socket binding/handling
        self.handler = DashboardHandler.__new__(DashboardHandler)
        self.handler.server = self.server
        self.handler.client_address = ('0.0.0.0', 8888)
        self.handler.requestline = 'POST /api/history HTTP/1.1'
        self.handler.command = 'POST'
        
        # Capture the response
        self.handler.wfile = MagicMock()
        self.handler.rfile = MagicMock()
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.send_error = MagicMock()

    def test_post_history_view_action(self):
        """Test the /api/history endpoint with 'view' action."""
        self.handler.path = '/api/history'
        self.handler.headers = {'Content-Length': '100'} # Arbitrary
        
        payload = json.dumps({"id": "prop1", "action": "view"}).encode('utf-8')
        self.handler.rfile.read.return_value = payload
        
        self.handler.do_POST()
        
        # Verify manager called
        self.server.history_manager.mark_seen.assert_called_with("prop1")
        
        # Verify response
        self.handler.send_response.assert_called_with(200)
        # Check written output
        args, _ = self.handler.wfile.write.call_args
        response_data = json.loads(args[0])
        self.assertEqual(response_data['status'], 'success')

    def test_post_history_dismiss_action(self):
        """Test the /api/history endpoint with 'dismiss' action."""
        self.handler.path = '/api/history'
        self.handler.headers = {'Content-Length': '100'} 
        
        payload = json.dumps({"id": "prop2", "action": "dismiss"}).encode('utf-8')
        self.handler.rfile.read.return_value = payload
        
        self.handler.do_POST()
        
        self.server.history_manager.mark_dismissed.assert_called_with("prop2")

    def test_post_history_invalid_action(self):
        """Test handling of invalid actions."""
        self.handler.path = '/api/history'
        self.handler.headers = {'Content-Length': '100'}
        
        payload = json.dumps({"id": "prop3", "action": "dance"}).encode('utf-8')
        self.handler.rfile.read.return_value = payload
        
        self.handler.do_POST()
        
        # Should return error or just success (depending on spec, let's say success but no op, or error)
        # Spec says: updates history.json based on action.
        # Let's assume we want it to error 400 for bad action.
        self.handler.send_error.assert_called_with(400, "Invalid action")

if __name__ == '__main__':
    unittest.main()
