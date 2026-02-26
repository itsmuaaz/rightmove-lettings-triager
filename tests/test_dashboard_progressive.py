import unittest
from unittest.mock import MagicMock
from dashboard import DashboardHandler
from search_state import SearchState
from http.server import HTTPServer

class TestDashboardProgressive(unittest.TestCase):
    def test_do_GET_sorts_properties(self):
        # Mock the server instance
        server = MagicMock(spec=HTTPServer)
        server.search_state = SearchState()
        
        # Prop 1: Commute 50 mins, Score 50
        p1 = {'id': '1', 'commute_time': 50, 'smart_score': 50}
        # Prop 2: Commute 10 mins, Score 80
        p2 = {'id': '2', 'commute_time': 10, 'smart_score': 80}
        # Prop 3: Loading (None), Score 20
        p3 = {'id': '3', 'commute_time': None, 'smart_score': 20}
        
        server.search_state.properties = [p1, p2, p3]
        server.search_state.total = 3
        server.search_state.processed = 1
        server.reporter = MagicMock()
        server.note_manager = MagicMock()
        server.history_manager = MagicMock()
        
        server.reporter.generate_report.return_value = "<html>Report</html>"

        handler = DashboardHandler.__new__(DashboardHandler)
        handler.server = server
        handler.request = MagicMock()
        handler.client_address = ('127.0.0.1', 8888)
        handler.wfile = MagicMock()
        handler.requestline = 'GET / HTTP/1.1'
        handler.request_version = 'HTTP/1.1'
        handler.path = '/'
        
        handler.do_GET()
        
        # Check argument passed to generate_report
        args, kwargs = server.reporter.generate_report.call_args
        passed_props = args[0]
        
        # Expected order: p2 (80), p1 (50), p3 (20) - Default DESC score
        self.assertEqual(passed_props[0]['id'], '2')
        self.assertEqual(passed_props[1]['id'], '1')
        self.assertEqual(passed_props[2]['id'], '3')

if __name__ == '__main__':
    unittest.main()
