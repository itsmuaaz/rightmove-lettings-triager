import unittest
from reporter import Reporter

class TestReporterDashboard(unittest.TestCase):
    def test_js_inclusion(self):
        """Test that the JavaScript for saving notes is included in the template."""
        reporter = Reporter()
        html = reporter.get_html_template()
        self.assertIn("function saveNote", html)
        self.assertIn("fetch('/api/notes'", html)

    def test_notes_column_header(self):
        """Test that the Notes column header is added."""
        reporter = Reporter()
        self.assertIn("Notes", reporter.headers)

    def test_notes_textarea_generation(self):
        """Test generation of the textarea for notes."""
        reporter = Reporter()
        prop = {
            'id': '12345',
            'price': '£1000',
            'note': 'Existing note content'
        }
        # Mock other fields to avoid errors
        row = reporter._generate_row(prop, for_html=True)
        
        self.assertIn('<textarea', row)
        self.assertIn("onblur=\"saveNote('12345', this.value)\"", row)
        self.assertIn('>Existing note content</textarea>', row)

    def test_notes_textarea_empty(self):
        """Test generation of empty textarea."""
        reporter = Reporter()
        prop = {'id': '67890'}
        row = reporter._generate_row(prop, for_html=True)
        
        self.assertIn('placeholder="Start typing..."', row)
        self.assertIn('></textarea>', row)

if __name__ == '__main__':
    unittest.main()
