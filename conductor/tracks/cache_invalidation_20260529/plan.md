# Implementation Plan - Revamp Cache Invalidation & TTL System

## Phase 1: TfL Cache Expiration & Audit Logging
- [ ] Task: Implement expiration checks in `tfl_client.py:_load_cache` (TDD - Red/Green)
    - [ ] Sub-task: Write unit tests with mocked times and mock cache files (one fresh, one stale) to verify `_load_cache` detects stale benchmarks.
    - [ ] Sub-task: Update `_load_cache` to parse and compare `arrival_benchmark` against current time (bypass and delete if stale).
- [ ] Task: Implement audit logging in `TflClient`
    - [ ] Sub-task: Add cleanly formatted `sys.stderr` logs for `[CACHE HIT]`, `[CACHE BYPASS - STALE]`, and `[CACHE FETCH]`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: TfL Cache Expiration & Audit Logging' (Protocol in workflow.md)

## Phase 2: Vibe Cache TTL & Configuration
- [ ] Task: Add TTL configuration and update Vibe schema (TDD - Red/Green)
    - [ ] Sub-task: Add `VIBE_CACHE_TTL_DAYS = 30` to `config.py`.
    - [ ] Sub-task: Write unit tests verifying that entries older than TTL are bypassed, and legacy entries (missing timestamp) are expired.
    - [ ] Sub-task: Update `VibeClient` to save `"cached_at"` timestamp with each entry in `.vibe_cache.json`.
    - [ ] Sub-task: Implement TTL validation check in `VibeClient` and add standard `[CACHE HIT]`, `[CACHE BYPASS - STALE]`, and `[CACHE MISS]` logging.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Vibe Cache TTL & Configuration' (Protocol in workflow.md)

## Phase 3: Automated Cache Maintenance Chore
- [ ] Task: Implement cache cleanup chore (TDD - Red/Green)
    - [ ] Sub-task: Write unit tests for the cleanup utility verifying it correctly scans `.tfl_cache` and deletes files with stale benchmarks.
    - [ ] Sub-task: Implement `cleanup_stale_caches(cache_dir)` in `tfl_client.py`.
    - [ ] Sub-task: Call `cleanup_stale_caches` at the start of `rightmove_search.py:main`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Automated Cache Maintenance Chore' (Protocol in workflow.md)