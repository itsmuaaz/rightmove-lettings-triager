# Implementation Plan - Progressive Results Loading

## Phase 1: State Management & Reporter Updates
- [ ] Task: Create `search_state.py` with `SearchState` class to hold `properties` list, `total_count`, and `processed_count` (TDD - Red/Green)
- [ ] Task: Update `DashboardHandler` in `dashboard.py` to accept and use a shared `SearchState` instance for rendering (Refactor)
- [ ] Task: Update `reporter.py` to handle `None` values for commute/amenities gracefully, rendering "Loading..." placeholders (TDD - Red/Green)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: State Management & Reporter Updates' (Protocol in workflow.md)

## Phase 2: Concurrent Execution Logic
- [ ] Task: Refactor `rightmove_search.py` to initialize `SearchState` with all raw properties immediately after fetching (Refactor)
- [ ] Task: Update `rightmove_search.py` to start the `HTTPServer` in a separate daemon thread *before* the processing loop begins (Refactor)
- [ ] Task: modifying the processing loop in `rightmove_search.py` to update the shared `SearchState` objects in real-time as each property finishes (Refactor)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Concurrent Execution Logic' (Protocol in workflow.md)

## Phase 3: UI Feedback & Controls
- [ ] Task: Update `templates/report.html` to display a sticky "Processing: X of Y... [Refresh]" banner (Jinja2)
- [ ] Task: Add a manual "Refresh Results" button to the banner that reloads the page (Jinja2)
- [ ] Task: Verify that sorting behaves correctly with mixed processed/unprocessed items (Manual)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: UI Feedback & Controls' (Protocol in workflow.md)
