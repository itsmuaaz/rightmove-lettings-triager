# Implementation Plan - Interactive Dashboard

## Phase 1: Storage Logic
- [ ] Task: Implement `NoteManager` class to handle `notes.json` operations (TDD - Red/Green)
    - [ ] Create `notes_manager.py` with methods to load, get, save notes.
    - [ ] Ensure atomic writes (or safe overwrites) for `notes.json`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Storage Logic' (Protocol in workflow.md)

## Phase 2: Server Infrastructure
- [ ] Task: Create `dashboard.py` implementing `DashboardHandler` (TDD - Red/Green)
    - [ ] Implement `do_GET` to serve content.
    - [ ] Implement `do_POST` to handle `/api/notes` and call `NoteManager`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Server Infrastructure' (Protocol in workflow.md)

## Phase 3: UI Integration & Main Loop
- [ ] Task: Update `Reporter` class to add "Notes" column and client-side JavaScript (TDD - Red/Green)
    - [ ] Add `<textarea>` and `fetch` logic to HTML template.
- [ ] Task: Update `rightmove_search.py` to start the server by default (TDD/Integration)
    - [ ] Replace exit with `server.serve_forever()`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: UI Integration & Main Loop' (Protocol in workflow.md)