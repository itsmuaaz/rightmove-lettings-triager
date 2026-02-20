# Specification: Interactive Dashboard & Persistent Notes

## Overview
Transform the static report generator into an interactive local dashboard. This allows users to add persistent notes to properties directly within the browser, which are saved across sessions.

## Functional Requirements
- **Web Server:** The script shall start a lightweight local HTTP server (using `http.server`) to serve the report and handle API requests.
- **Persistent Storage:** Notes shall be stored in a `notes.json` file in the project root, keyed by the unique Rightmove Property ID.
- **Interactive UI:**
    - Add a new "Notes" column to the HTML report.
    - Include an editable `<textarea>` for each property.
    - Implement auto-save functionality (via JavaScript `fetch`) triggered on input or blur.
- **Data Persistence:** On generation, the script must read `notes.json` and pre-fill the text areas with existing notes.
- **Default Mode:** The server mode shall be the default behavior when running the script.

## Non-Functional Requirements
- **Dependencies:** STRICTLY use Python standard libraries (no Flask/Django).
- **Security:** Bind the server to `127.0.0.1` (localhost) only.
- **Port:** Default to port 8000.

## Acceptance Criteria
1. Running `python rightmove_search.py <URL>` starts the server and keeps running.
2. The report contains a "Notes" column with editable text areas.
3. Reloading the page or restarting the script preserves the notes.
4. `notes.json` is correctly updated on disk after editing a note.