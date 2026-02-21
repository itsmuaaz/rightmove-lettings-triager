# Implementation Plan - Multi-Portal Architecture Refactor

## Phase 1: Standardization & Decoupling
- [ ] Task: Create `models.py` with `Property` TypedDict to enforce standard schema (TDD - Red/Green)
- [ ] Task: Refactor `CommuteCalculator` to accept `latitude` and `longitude` instead of raw dict (TDD - Red/Green)
- [ ] Task: Update `Reporter` to handle absolute URLs and remove hardcoded `rightmove.co.uk` prefixes (TDD - Red/Green)
- [ ] Task: Update `rightmove_search.py` to populate the full `Property` schema (including absolute URLs) (Refactor)
- [ ] Task: Verify existing functionality ensures no regressions (Manual)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Standardization & Decoupling' (Protocol in workflow.md)

## Phase 2: Portal Extraction
- [ ] Task: Create `portals/` package and define `PropertySource` ABC in `portals/base.py` (TDD - Red/Green)
- [ ] Task: Extract scraping logic from `rightmove_search.py` into `portals/rightmove.py` implementing `RightmoveClient` (Refactor)
- [ ] Task: Add tests for `RightmoveClient` to verify it correctly fetches and parses properties (TDD - Red/Green)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Portal Extraction' (Protocol in workflow.md)

## Phase 3: Generic Runner
- [ ] Task: Rename `rightmove_search.py` to `search.py` (Chore)
- [ ] Task: Implement `ClientFactory` to select `RightmoveClient` based on URL (TDD - Red/Green)
- [ ] Task: Update `search.py` to use `ClientFactory` and run the generic search loop (Integration)
- [ ] Task: Ensure all tests pass and coverage is >80% (Verification)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Generic Runner' (Protocol in workflow.md)
