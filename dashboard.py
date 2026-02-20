from http.server import BaseHTTPRequestHandler
import json

class DashboardHandler(BaseHTTPRequestHandler):
    """Handles HTTP requests for the dashboard."""

    def do_GET(self):
        """Serve the HTML report."""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Serve the generated HTML content from the server instance
            if hasattr(self.server, 'html_content'):
                self.wfile.write(self.server.html_content.encode('utf-8'))
            else:
                self.wfile.write(b"No report generated.")
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        """Handle note updates."""
        if self.path == '/api/notes':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                property_id = data.get('id')
                note_content = data.get('note')
                
                if property_id and hasattr(self.server, 'note_manager'):
                    self.server.note_manager.save_note(property_id, note_content)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
                else:
                    self.send_error(400, "Invalid request or missing NoteManager")
            except Exception as e:
                self.send_error(500, f"Server error: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        """Suppress default logging to keep CLI clean."""
        return
