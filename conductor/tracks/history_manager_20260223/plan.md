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
- [x] Task: Update `DashboardHandler.do_POST` in `dashboard.py` to handle `/api/history` [06a7bd0]
    - [x] Handle actions: `view`, `dismiss`, `undo_dismiss`
    - [x] Return updated status in JSON response
- [x] Task: Update main scraping loop (`main.py` equivalent or where `properties` are processed) [25804f3]
    - [x] Initialize `HistoryManager`
    - [x] On scrape completion, update history with new IDs (`status=new`)
- [x] Task: Conductor - User Manual Verification 'Phase 2: API & Scraper Integration' (Protocol in workflow.md) [checkpoint: 95fc34c]

## Phase 3: Frontend Implementation
- [x] Task: Update `reporter.py` to inject `history_status` into property objects passed to template [bea3769]
- [x] Task: Update HTML/CSS in `reporter.py` (or template file) [bea3769]
    - [x] Add CSS classes: `.status-new`, `.status-viewed`, `.status-dismissed`
    - [x] Add "NEW" badge element
    - [x] Add "Dismiss" button
    - [x] Add "Undo Dismiss" button (visible on collapsed state)
- [x] Task: Implement Frontend Logic (JavaScript) [bea3769]
    - [x] Attach `onclick` to "View on Rightmove" -> Call API `view` -> Add `.status-viewed`
    - [x] Attach `onclick` to "Dismiss" -> Call API `dismiss` -> Add `.status-dismissed` (collapse card)
    - [x] Attach `onclick` to "Undo" -> Call API `undo_dismiss` -> Remove `.status-dismissed` (expand card)
    - [x] Implement "Mark All Visible as Seen" button logic
- [x] Task: Conductor - User Manual Verification 'Phase 3: Frontend Implementation' (Protocol in workflow.md) [checkpoint: 4cb533e]

## Phase 4: Final Polish & Documentation
- [x] Task: Update `product.md` and `tech-stack.md` to reflect new architecture [c5fb264]
- [x] Task: Final End-to-End Verification (Scrape -> View -> Restart -> Verify State) [06586a4]
- [x] Task: Conductor - User Manual Verification 'Phase 4: Final Polish & Documentation' (Protocol in workflow.md) [checkpoint: c2f78a1]

## Phase: Review Fixes
- [x] Task: Apply review suggestions [c434a20]
- [x] Task: Fix logic regression in rightmove_search.py [bb4b0f9]
