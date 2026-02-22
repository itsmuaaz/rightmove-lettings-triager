# Design Document: Interactive Dashboard for Persistent Notes

## 1. Overview
The goal is to transform the existing static HTML report generation (`results.html`) into an interactive local dashboard. This allows users to add persistent notes to properties directly within the browser, which are saved across sessions without requiring manual file edits or complex databases.

## 2. Architecture

### 2.1 Core Components
1.  **Server (Python):** A lightweight HTTP server using the standard library `http.server`. It serves the report and handles API requests to save notes.
2.  **Client (HTML/JS):** The existing report, enhanced with a "Notes" column containing editable text areas and vanilla JavaScript to communicate with the server.
3.  **Storage (JSON):** A local file (`notes.json`) storing notes keyed by property ID.

### 2.2 Constraints
-   **No External Frameworks:** Must use Python standard library (no Flask/Django).
-   **Single User:** Designed for local use by one person.
-   **Minimal Dependencies:** Keep the project lightweight.

## 3. Data Flow

### 3.1 Loading the Dashboard (GET /)
1.  User runs `python rightmove_search.py --serve`.
2.  Server starts on `localhost:8000`.
3.  Browser requests `GET /`.
4.  Server:
    a.  Runs the search logic (or uses cached results).
    b.  Reads `notes.json` from disk.
    c.  Generates the HTML table, injecting existing notes into the corresponding rows.
    d.  Serves the complete HTML page.

### 3.2 Saving a Note (POST /api/notes)
1.  User types in a note for Property ID `12345`.
2.  JavaScript detects the change (e.g., `onblur` or debounce).
3.  JavaScript sends a `POST` request to `/api/notes` with payload: `{"id": "12345", "note": "Great garden!"}`.
4.  Server:
    a.  Receives the request.
    b.  Reads `notes.json`.
    c.  Updates the entry for `12345`.
    d.  Writes `notes.json` back to disk atomically.
    e.  Returns `200 OK`.

## 4. Implementation Details

### 4.1 Storage Schema (`notes.json`)
```json
{
  "87492011": {
    "content": "Booked viewing for Tuesday.",
    "updated_at": "2026-02-21T09:30:00"
  },
  "99283744": {
    "content": "Too expensive, maybe negotiate?",
    "updated_at": "2026-02-20T10:00:00"
  }
}
```

### 4.2 Server Logic (`dashboard.py` or integrated)
We will implement a custom handler inheriting from `http.server.BaseHTTPRequestHandler`:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # 1. Generate report data
            # 2. Inject notes
            # 3. Serve HTML
            self.send_response(200)
            self.end_headers()
            self.wfile.write(html_content.encode())

    def do_POST(self):
        if self.path == '/api/notes':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            # Save data['note'] for data['id']
            save_note(data['id'], data['note'])
            self.send_response(200)
            self.end_headers()
```

### 4.3 Client-Side JavaScript
Inject this script into the HTML `head` or body:

```javascript
function saveNote(propertyId, text) {
    fetch('/api/notes', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: propertyId, note: text})
    }).then(response => {
        if (response.ok) {
            console.log('Note saved');
            // Optional: Show "Saved" indicator
        } else {
            console.error('Failed to save');
        }
    });
}
```

And update the HTML row generation:
```html
<td>
    <textarea onblur="saveNote('12345', this.value)">Pre-filled note...</textarea>
</td>
```

## 5. Security & Concurrency
-   **Binding:** Bind to `127.0.0.1` (localhost) only to prevent network access.
-   **Concurrency:** Since it's a single-user local tool, race conditions are rare. We use simple file overwrites. For robustness, we can write to a temp file and rename (atomic write) to avoid corruption if the script crashes mid-write.

## 6. Future Extensibility
-   **Hide Properties:** Add a "Hide" button that marks a property as `hidden: true` in `notes.json`, filtering it out from future views.
-   **Favorites:** Add a "Star" button.
-   **Tags:** Add `#tag` support in notes for filtering.
