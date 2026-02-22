# Implementation Plan - TfL Client Optimization

## Phase 1: Caching Infrastructure
- [x] Task: Implement `_get_cache_key` and `_load_cache`/`_save_cache` methods in `TflClient` (TDD - Red/Green) [e71a55f]
- [x] Task: Update `_fetch_journey` to check and write to cache (Refactor) [6168d29]
- [x] Task: Verify caching avoids network calls on repeat requests (TDD - Green) [b7d26cd]
- [x] Task: Conductor - User Manual Verification 'Phase 1: Caching Infrastructure' (Protocol in workflow.md) [checkpoint: 971c5c3]

## Phase 2: Rate Limiting & Resilience
- [x] Task: Implement thread-safe `_wait_for_slot` method using `threading.Lock` (TDD - Red/Green) [52e217a]
- [x] Task: Integrate rate limiting into `_fetch_journey` (Refactor) [beab4ee]
- [x] Task: Improve 429 error handling with aggressive backoff (Refactor) [c01d63b]
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Rate Limiting & Resilience' (Protocol in workflow.md)
