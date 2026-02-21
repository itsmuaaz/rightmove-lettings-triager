# Implementation Plan - Interactive Dashboard

## Phase 1: Storage Logic [checkpoint: 3894d22]
- [x] Task: Implement `NoteManager` class to handle `notes.json` operations (TDD - Red/Green) 5b01060
    - [x] Create `notes_manager.py` with methods to load, get, save notes. 5b01060
    - [x] Ensure atomic writes (or safe overwrites) for `notes.json`. 5b01060
- [x] Task: Conductor - User Manual Verification 'Phase 1: Storage Logic' (Protocol in workflow.md) 3894d22

## Phase 2: Server Infrastructure [checkpoint: f41c48f]
- [x] Task: Create `dashboard.py` implementing `DashboardHandler` (TDD - Red/Green) 372a8a6
    - [x] Implement `do_GET` to serve content. 372a8a6
    - [x] Implement `do_POST` to handle `/api/notes` and call `NoteManager`. 372a8a6
- [x] Task: Conductor - User Manual Verification 'Phase 2: Server Infrastructure' (Protocol in workflow.md) f41c48f

## Phase 3: UI Integration & Main Loop
- [ ] Task: Update `Reporter` class to add "Notes" column and client-side JavaScript (TDD - Red/Green)
    - [ ] Add `<textarea>` and `fetch` logic to HTML template.
- [ ] Task: Update `rightmove_search.py` to start the server by default (TDD/Integration)
    - [ ] Replace exit with `server.serve_forever()`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: UI Integration & Main Loop' (Protocol in workflow.md)