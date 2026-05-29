# Implementation Plan - Cache Partitioning & Targeted Threading

## Phase 1: Cache Checking & Partitioning Logic
- [x] Task: Create helper functions `is_tfl_cached`, `is_osm_cached`, and `is_vibe_cached` in `rightmove_search.py` (TDD - Red/Green) [5c59630]
- [x] Task: Create unit tests in `tests/test_cache_partitioning.py` to verify cache detection functions (TDD - Red) [5c59630]
- [x] Task: Implement unified `is_fully_cached` logic checking all three caches (TDD - Green) [5c59630]
- [x] Task: Implement synchronous processing logic to populate fully cached property details instantly (TDD - Red/Green) [5c59630]
- [x] Task: Conductor - User Manual Verification 'Phase 1: Cache Checking & Partitioning Logic' (Protocol in workflow.md) [checkpoint: aa137c6]

## Phase 2: Targeted Threading & Integration
- [ ] Task: Integrate partitioning pass into `rightmove_search.py` main loop before ThreadPoolExecutor startup (Integration)
- [ ] Task: Ensure `ThreadPoolExecutor` is completely bypassed if all properties are cached, proceeding instantly to server start (Integration)
- [ ] Task: Bulk-update the progressive dashboard progress counter (`search_state.processed`) after processing synchronous properties (Integration)
- [ ] Task: Create integration tests verifying the full partitioned run from scrape to server-ready state (Integration)
- [ ] Task: Run full test suite and verify no regressions in scoring, sorting, or server endpoints (Verification)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Targeted Threading & Integration' (Protocol in workflow.md)