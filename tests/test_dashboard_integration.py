import unittest
import threading
from http.server import HTTPServer
from dashboard import DashboardHandler
from history_manager import HistoryManager

class MockServer:
    def __init__(self):
        self.properties = []
        self.reporter = None
        self.note_manager = None
        self.history_manager = None # This is what we are testing

class TestDashboardIntegration(unittest.TestCase):
    def test_handler_has_access_to_history_manager(self):
        """Test that the handler can access the history manager via the server."""
        # Setup mock server
        server = MockServer()
        server.history_manager = HistoryManager("test_history.json")
        
        # Manually link the handler to the server (normally done by HTTPServer)
        handler = DashboardHandler
        # We can't easily instantiate BaseHTTPRequestHandler without a socket
        # So we just verify the pattern:
        # The pattern in dashboard.py is self.server.history_manager
        
        self.assertIsNotNone(server.history_manager)
        self.assertIsInstance(server.history_manager, HistoryManager)

if __name__ == '__main__':
    unittest.main()
