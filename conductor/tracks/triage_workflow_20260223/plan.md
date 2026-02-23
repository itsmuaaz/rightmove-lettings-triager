# Implementation Plan - Triage Workflow

## Phase 1: Backend Support for Shortlisting
- [x] Task: Update `HistoryManager` in `history_manager.py` (TDD - Red/Green) e8af081
    - [x] Add `mark_shortlisted(property_id)` method.
    - [x] Update `mark_seen(property_id)` to respect `shortlisted` state (don't overwrite it).
    - [x] Test transitions: `new` -> `shortlisted`, `viewed` -> `shortlisted`, `shortlisted` -> `viewed` (should stay shortlisted).
- [x] Task: Update `DashboardHandler` in `dashboard.py` to handle `action: shortlist`. 84dacfc
- [~] Task: Conductor - User Manual Verification 'Phase 1: Backend Support' (Protocol in workflow.md)

## Phase 2: Frontend Implementation
- [ ] Task: Update `reporter.py` CSS/JS
    - [ ] Add `.status-shortlisted` style (gold border, full opacity).
    - [ ] Update `markViewed` JS function to check if item is shortlisted before applying `.status-viewed`.
    - [ ] Implement `markShortlisted` JS function.
- [ ] Task: Update `reporter.py` HTML generation
    - [ ] Add "Star" button to `_generate_html_row`.
    - [ ] Ensure correct initial class is applied if property is already shortlisted.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Frontend Implementation' (Protocol in workflow.md)

## Phase 3: Final Integration & Polish
- [ ] Task: Update `product.md` to reflect the new Triage workflow.
- [ ] Task: Final End-to-End Verification (Shortlist -> Restart -> Verify Persistence).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Integration' (Protocol in workflow.md)