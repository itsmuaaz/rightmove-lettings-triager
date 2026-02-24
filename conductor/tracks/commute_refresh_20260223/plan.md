# Implementation Plan - Commute Stability & Force Refresh

## Phase 1: TfL Client & Caching Enhancements [checkpoint: 4f53848]
- [x] Task: Create `benchmark_utils.py` with `get_next_benchmark_time()` function (TDD - Red/Green) b0580c9
    - [x] Unit tests for: Monday -> Next Tue 9AM, Tuesday 8AM -> Today 9AM, Tuesday 10AM -> Next Tue 9AM.
- [x] Task: Update `TflClient` in `tfl_client.py` for metadata caching (TDD - Red/Green) 27e846b
    - [x] Update `_save_cache` and `_load_cache` to handle the new JSON wrapper.
    - [x] Ensure legacy files are ignored or deleted if they don't match the new structure.
- [x] Task: Update `TflClient.get_commute_time` to use benchmark parameters (TDD - Red/Green) 261d84d
    - [x] Inject `date`, `time`, and `timeIs=Arriving` into the TfL API request.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Client Enhancements' (Protocol in workflow.md) 4f53848

## Phase 2: Backend Support (API) [checkpoint: 9ad8ece]
- [x] Task: Implement `force_refresh` flag in `TflClient._fetch_journey` (TDD - Red/Green) 1019263
    - [x] Ensure `force_refresh=True` bypasses `_load_cache` but still calls `_save_cache`.
- [x] Task: Update `DashboardHandler.do_POST` in `dashboard.py` to handle `/api/refresh` (TDD - Red/Green) dede488
    - [x] Endpoint should accept `{ "id": "property_id" }`.
    - [x] Trigger re-calculation and return the updated property data with timestamp.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Backend Support' (Protocol in workflow.md) 9ad8ece

## Phase 3: Frontend Implementation (Dashboard) [checkpoint: ca8b2eb]
- [x] Task: Update `reporter.py` CSS/HTML to include refresh icons and timestamps (TDD - Red/Green) ed4cf92
    - [x] Add `.refresh-icon` (🔄) next to commute badges.
    - [x] Add `.calc-timestamp` label (e.g., "14:30") near badges.
    - [x] Add "Refresh All" button to the header.
- [x] Task: Implement JavaScript `refreshProperty(id)` in `reporter.py` template (TDD-like) ed4cf92
    - [x] Call `/api/refresh`, show loading state, and update cell content on success.
- [x] Task: Implement JavaScript `refreshAll()` to sequentially update all properties (TDD-like) ed4cf92
    - [x] Iterate through all property IDs and call `refreshProperty` for each.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Frontend Implementation' (Protocol in workflow.md) ca8b2eb

## Phase 4: Final Polish & Documentation
- [x] Task: Update `product.md` and `tech-stack.md` to reflect commute stability changes. c79b91e
- [x] Task: Final End-to-End Verification (Scrape -> Refresh -> Verify Cache Metadata). 8638
- [x] Task: Conductor - User Manual Verification 'Phase 4: Final Polish' (Protocol in workflow.md)
