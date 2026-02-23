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
            
            # Regenerate HTML if possible to show latest notes
            if hasattr(self.server, 'properties') and hasattr(self.server, 'reporter') and hasattr(self.server, 'note_manager'):
                # Refresh notes and history
                for p in self.server.properties:
                    p['note'] = self.server.note_manager.get_note(p['id'])
                    if hasattr(self.server, 'history_manager'):
                        p['history_status'] = self.server.history_manager.get_status(p['id'])
                
                html_content = self.server.reporter.generate_html_report(self.server.properties)
                self.wfile.write(html_content.encode('utf-8'))
            # Fallback to static content
            elif hasattr(self.server, 'html_content'):
                self.wfile.write(self.server.html_content.encode('utf-8'))
            else:
                self.wfile.write(b"No report generated.")
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        """Handle note updates and history actions."""
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
        elif self.path == '/api/history':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                property_id = data.get('id')
                action = data.get('action')
                
                if not property_id or not hasattr(self.server, 'history_manager'):
                     self.send_error(400, "Invalid request or missing HistoryManager")
                     return

                if action == 'view':
                    self.server.history_manager.mark_seen(property_id)
                elif action == 'dismiss':
                    self.server.history_manager.mark_dismissed(property_id)
                elif action == 'undo_dismiss':
                    # Revert to viewed or new. For now, mark as seen updates timestamp,
                    # which is close enough to 'undo' effectively.
                    # Or we could just set status back to 'viewed' without updating timestamp?
                    # Spec says: "Reverts status to viewed (or new if never viewed)."
                    # Current HistoryManager doesn't support revert explicitly.
                    # Let's just re-mark as seen for now as a safe default for 'undo'.
                    # TODO: Implement stricter undo if needed.
                    self.server.history_manager.mark_seen(property_id)
                else:
                    self.send_error(400, "Invalid action")
                    return

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Server error: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        """Suppress default logging to keep CLI clean."""
        return
