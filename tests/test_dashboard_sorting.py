import unittest
from unittest.mock import MagicMock
from io import BytesIO
from dashboard import DashboardHandler

class TestDashboardSorting(unittest.TestCase):
    def setUp(self):
        class MockServer:
            pass
        self.mock_server = MockServer()
        self.mock_server.note_manager = MagicMock()
        self.mock_server.history_manager = MagicMock()
        self.mock_server.reporter = MagicMock()
        self.mock_server.reporter.generate_report.return_value = "<html>Sorted</html>"
        
        # Sample properties
        self.props = [
            {'id': '1', 'price': 1000, 'smart_score': 50, 'commute_time': 30, 'commute_cycling': 20, 'vibe_score': 5},
            {'id': '2', 'price': 2000, 'smart_score': 80, 'commute_time': 60, 'commute_cycling': 15, 'vibe_score': 8},
            {'id': '3', 'price': 1500, 'smart_score': 60, 'commute_time': 45, 'commute_cycling': 45, 'vibe_score': 6}
        ]
        self.mock_server.properties = self.props
        
        # Default mock returns
        self.mock_server.note_manager.get_note.return_value = ""
        self.mock_server.history_manager.get_status.return_value = "new"

    def _make_handler(self, path='/'):
        handler = DashboardHandler.__new__(DashboardHandler)
        handler.server = self.mock_server
        handler.request = MagicMock()
        handler.client_address = ('127.0.0.1', 8888)
        
        handler.path = path
        handler.command = 'GET'
        handler.requestline = f"GET {path} HTTP/1.1"
        handler.request_version = "HTTP/1.1"
        handler.protocol_version = "HTTP/1.1"
        
        handler.rfile = BytesIO()
        handler.wfile = BytesIO()
        handler.headers = {}
        
        return handler

    def test_sort_by_price_asc(self):
        handler = self._make_handler('/?sort=price&order=asc')
        handler.do_GET()
        
        args, _ = self.mock_server.reporter.generate_report.call_args
        sorted_props = args[0]
        ids = [p['id'] for p in sorted_props]
        self.assertEqual(ids, ['1', '3', '2']) # 1000, 1500, 2000

    def test_sort_by_price_desc(self):
        handler = self._make_handler('/?sort=price&order=desc')
        handler.do_GET()
        
        args, _ = self.mock_server.reporter.generate_report.call_args
        sorted_props = args[0]
        ids = [p['id'] for p in sorted_props]
        self.assertEqual(ids, ['2', '3', '1']) # 2000, 1500, 1000

    def test_sort_by_smart_score_desc(self):
        # Spec says default smart score High <-> Low (DESC)
        handler = self._make_handler('/?sort=smart_score&order=desc')
        handler.do_GET()
        
        args, _ = self.mock_server.reporter.generate_report.call_args
        sorted_props = args[0]
        ids = [p['id'] for p in sorted_props]
        self.assertEqual(ids, ['2', '3', '1']) # 80, 60, 50

    def test_sort_by_commute_min(self):
        # min(30,20)=20, min(60,15)=15, min(45,45)=45
        # ASC: 15 (id 2), 20 (id 1), 45 (id 3)
        handler = self._make_handler('/?sort=commute&mode=min&order=asc')
        handler.do_GET()
        
        args, _ = self.mock_server.reporter.generate_report.call_args
        sorted_props = args[0]
        ids = [p['id'] for p in sorted_props]
        self.assertEqual(ids, ['2', '1', '3'])

    def test_sort_by_commute_transport(self):
        # 30 (id 1), 60 (id 2), 45 (id 3)
        # ASC: 30 (1), 45 (3), 60 (2)
        handler = self._make_handler('/?sort=commute&mode=transport&order=asc')
        handler.do_GET()
        
        args, _ = self.mock_server.reporter.generate_report.call_args
        sorted_props = args[0]
        ids = [p['id'] for p in sorted_props]
        self.assertEqual(ids, ['1', '3', '2'])

    def test_default_sort(self):
        # Spec: Default is Smart Score Descending
        handler = self._make_handler('/')
        handler.do_GET()
        
        args, _ = self.mock_server.reporter.generate_report.call_args
        sorted_props = args[0]
        ids = [p['id'] for p in sorted_props]
        self.assertEqual(ids, ['2', '3', '1']) # 80, 60, 50
