# Implementation Plan - History Manager

## Phase 1: History Infrastructure (Backend)
- [x] Task: Create `HistoryManager` class in `history_manager.py` (TDD - Red/Green) [f98e7e6]
    - [x] Implement `load_history` and `save_history` (JSON persistence)
    - [x] Implement `mark_seen(property_id)`
    - [x] Implement `mark_dismissed(property_id)`
    - [x] Implement `get_status(property_id)`
- [x] Task: Integrate `HistoryManager` into `dashboard.py` (Dependency Injection) [947d6ca]
- [x] Task: Conductor - User Manual Verification 'Phase 1: History Infrastructure' (Protocol in workflow.md) [checkpoint: c38f6b9]

## Phase 2: API & Scraper Integration
- [ ] Task: Update `DashboardHandler.do_POST` in `dashboard.py` to handle `/api/history`
    - [ ] Handle actions: `view`, `dismiss`, `undo_dismiss`
    - [ ] Return updated status in JSON response
- [ ] Task: Update main scraping loop (`main.py` equivalent or where `properties` are processed)
    - [ ] Initialize `HistoryManager`
    - [ ] On scrape completion, update history with new IDs (`status=new`)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: API & Scraper Integration' (Protocol in workflow.md)

## Phase 3: Frontend Implementation
- [ ] Task: Update `reporter.py` to inject `history_status` into property objects passed to template
- [ ] Task: Update HTML/CSS in `reporter.py` (or template file)
    - [ ] Add CSS classes: `.status-new`, `.status-viewed`, `.status-dismissed`
    - [ ] Add "NEW" badge element
    - [ ] Add "Dismiss" button
    - [ ] Add "Undo Dismiss" button (visible on collapsed state)
- [ ] Task: Implement Frontend Logic (JavaScript)
    - [ ] Attach `onclick` to "View on Rightmove" -> Call API `view` -> Add `.status-viewed`
    - [ ] Attach `onclick` to "Dismiss" -> Call API `dismiss` -> Add `.status-dismissed` (collapse card)
    - [ ] Attach `onclick` to "Undo" -> Call API `undo_dismiss` -> Remove `.status-dismissed` (expand card)
    - [ ] Implement "Mark All Visible as Seen" button logic
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Frontend Implementation' (Protocol in workflow.md)

## Phase 4: Final Polish & Documentation
- [ ] Task: Update `product.md` and `tech-stack.md` to reflect new architecture
- [ ] Task: Final End-to-End Verification (Scrape -> View -> Restart -> Verify State)
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Polish & Documentation' (Protocol in workflow.md)