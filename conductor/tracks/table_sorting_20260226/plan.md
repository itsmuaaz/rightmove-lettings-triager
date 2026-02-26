# Implementation Plan - Table Sorting & Commute Optimization

## Phase 1: Backend Sort Logic [checkpoint: 55596a2]
- [x] Task: Create sort key factory in `utils.py`
    - [x] Sub-task: Write Tests (verify factory returns correct key for price, score, date, and commute modes)
    - [x] Sub-task: Implement Feature (Add `create_sort_key` function handling all sort modes)
- [x] Task: Update `DashboardHandler` to parse query parameters
    - [x] Sub-task: Write Tests (Simulate GET requests with `?sort=...` and verify property order)
    - [x] Sub-task: Implement Feature (Parse URL params in `do_GET` and use `create_sort_key` for sorting)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Backend Sort Logic' (Protocol in workflow.md)

## Phase 2: Frontend Implementation [checkpoint: afe5fc7]
- [x] Task: Update `report.html` headers
    - [x] Sub-task: Implement Feature (Make headers clickable links with dynamic URL generation)
    - [x] Sub-task: Implement Feature (Add sorting arrows CSS/Logic based on current state)
- [x] Task: Implement Commute Column Dropdown
    - [x] Sub-task: Implement Feature (Add UI for 'Transport', 'Cycling', 'Min' selection)
    - [x] Sub-task: Implement Feature (Ensure selection updates URL `mode` parameter)
- [x] Task: Conductor - User Manual Verification 'Phase 2: Frontend Implementation' (Protocol in workflow.md)

## Phase 3: Integration & Verification
- [ ] Task: Verify Sorting Behavior
    - [ ] Sub-task: Manual Verification (Click all headers, verify order)
    - [ ] Sub-task: Manual Verification (Verify persistence on refresh)
    - [ ] Sub-task: Manual Verification (Verify default state is Smart Score Descending)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Integration & Verification' (Protocol in workflow.md)
