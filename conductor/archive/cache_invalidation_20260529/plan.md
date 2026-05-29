# Implementation Plan - Revamp Cache Invalidation & TTL System

## Phase 1: TfL Cache Expiration & Audit Logging
- [x] Task: Implement expiration checks in `tfl_client.py:_load_cache` (TDD - Red/Green)
    - [x] Sub-task: Write unit tests with mocked times and mock cache files (one fresh, one stale) to verify `_load_cache` detects stale benchmarks.
    - [x] Sub-task: Update `_load_cache` to parse and compare `arrival_benchmark` against current time (bypass and delete if stale).
- [x] Task: Implement audit logging in `TflClient`
    - [x] Sub-task: Add cleanly formatted `sys.stderr` logs for `[CACHE HIT]`, `[CACHE BYPASS - STALE]`, and `[CACHE FETCH]`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: TfL Cache Expiration & Audit Logging' (Protocol in workflow.md)

## Phase 2: Vibe Cache TTL & Configuration
- [x] Task: Add TTL configuration and update Vibe schema (TDD - Red/Green)
    - [x] Sub-task: Add `VIBE_CACHE_TTL_DAYS = 30` to `config.py`.
    - [x] Sub-task: Write unit tests verifying that entries older than TTL are bypassed, and legacy entries (missing timestamp) are expired.
    - [x] Sub-task: Update `VibeClient` to save `"cached_at"` timestamp with each entry in `.vibe_cache.json`.
    - [x] Sub-task: Implement TTL validation check in `VibeClient` and add standard `[CACHE HIT]`, `[CACHE BYPASS - STALE]`, and `[CACHE MISS]` logging.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Vibe Cache TTL & Configuration' (Protocol in workflow.md)

## Phase 3: Automated Cache Maintenance Chore
- [x] Task: Implement cache cleanup chore (TDD - Red/Green)
    - [x] Sub-task: Write unit tests for the cleanup utility verifying it correctly scans `.tfl_cache` and deletes files with stale benchmarks.
    - [x] Sub-task: Implement `cleanup_stale_caches(cache_dir)` in `tfl_client.py`.
    - [x] Sub-task: Call `cleanup_stale_caches` at the start of `rightmove_search.py:main`.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Automated Cache Maintenance Chore' (Protocol in workflow.md)