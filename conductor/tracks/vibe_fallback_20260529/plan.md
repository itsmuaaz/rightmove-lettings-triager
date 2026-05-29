# Implementation Plan - Fix Vibe Scoring & Address Fallback

## Phase 1: Reverse-Geocoding Utility & Caching
- [ ] Task: Implement `reverse_geocode(lat, lon)` in `utils.py` (TDD - Red/Green)
    - [ ] Sub-task: Write unit tests verifying successful geocoding, timeout, and network errors.
    - [ ] Sub-task: Implement `reverse_geocode` with a 3-second timeout using standard urllib.
    - [ ] Sub-task: Implement in-memory cache to store coordinate-to-postcode mappings.
- [ ] Task: Update `extract_location_for_vibe` in `utils.py` (TDD - Red/Green)
    - [ ] Sub-task: Write unit tests verifying that descriptive addresses fallback to reverse-geocoding using coordinates.
    - [ ] Sub-task: Update `extract_location_for_vibe` to accept optional `latitude` and `longitude` and call `reverse_geocode`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Reverse-Geocoding Utility & Caching' (Protocol in workflow.md)

## Phase 2: Thread-Safe Vibe Caching
- [ ] Task: Implement thread locking in `VibeClient` (TDD - Red/Green)
    - [ ] Sub-task: Write unit tests simulating concurrent threads calling `get_vibes` to verify cache consistency and no deadlocks.
    - [ ] Sub-task: Initialize `threading.Lock` in `VibeClient.__init__`.
    - [ ] Sub-task: Guard all read/write access to `self.cache` and `self._save_cache()` using the lock.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Thread-Safe Vibe Caching' (Protocol in workflow.md)

## Phase 3: Integration & Final Verification
- [ ] Task: Integrate fallback coordinates in main search loop
    - [ ] Sub-task: Update `rightmove_search.py` processing to pass latitude and longitude to `extract_location_for_vibe`.
- [ ] Task: Verify results and performance
    - [ ] Sub-task: Run search manually and confirm that properties with descriptive addresses successfully retrieve non-N/A vibe scores.
    - [ ] Sub-task: Ensure modified modules maintain >80% test coverage and the test suite passes.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Integration & Final Verification' (Protocol in workflow.md)