# Implementation Plan - Commute Stability & Force Refresh

## Phase 1: TfL Client & Caching Enhancements
- [x] Task: Create `benchmark_utils.py` with `get_next_benchmark_time()` function (TDD - Red/Green) b0580c9
    - [ ] Unit tests for: Monday -> Next Tue 9AM, Tuesday 8AM -> Today 9AM, Tuesday 10AM -> Next Tue 9AM.
- [x] Task: Update `TflClient` in `tfl_client.py` for metadata caching (TDD - Red/Green) 27e846b
    - [ ] Update `_save_cache` and `_load_cache` to handle the new JSON wrapper.
    - [ ] Ensure legacy files are ignored or deleted if they don't match the new structure.
- [x] Task: Update `TflClient.get_commute_time` to use benchmark parameters (TDD - Red/Green) 261d84d
    - [ ] Inject `date`, `time`, and `timeIs=Arriving` into the TfL API request.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Client Enhancements' (Protocol in workflow.md)

## Phase 2: Backend Support (API)
- [ ] Task: Implement `force_refresh` flag in `TflClient._fetch_journey` (TDD - Red/Green)
    - [ ] Ensure `force_refresh=True` bypasses `_load_cache` but still calls `_save_cache`.
- [ ] Task: Update `DashboardHandler.do_POST` in `dashboard.py` to handle `/api/refresh` (TDD - Red/Green)
    - [ ] Endpoint should accept `{ "id": "property_id" }`.
    - [ ] Trigger re-calculation and return the updated property data with timestamp.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Backend Support' (Protocol in workflow.md)

## Phase 3: Frontend Implementation (Dashboard UI)
- [ ] Task: Update `reporter.py` CSS/HTML to include refresh icons and timestamps (TDD - Red/Green)
    - [ ] Add `.refresh-icon` (🔄) next to commute badges.
    - [ ] Add `.calc-timestamp` label (e.g., "14:30") near badges.
    - [ ] Add "Refresh All" button to the header.
- [ ] Task: Implement JavaScript `refreshProperty(id)` in `reporter.py` template (TDD-like)
    - [ ] Call `/api/refresh`, show loading state, and update cell content on success.
- [ ] Task: Implement JavaScript `refreshAll()` to sequentially update all properties (TDD-like)
    - [ ] Iterate through all property IDs and call `refreshProperty` for each.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Frontend Implementation' (Protocol in workflow.md)

## Phase 4: Final Polish & Documentation
- [ ] Task: Update `product.md` and `tech-stack.md` to reflect commute stability changes.
- [ ] Task: Final End-to-End Verification (Scrape -> Refresh -> Verify Cache Metadata).
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Polish' (Protocol in workflow.md)
