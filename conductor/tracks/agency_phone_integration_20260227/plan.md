# Implementation Plan - Agency Name and Phone Number

## Phase 1: Data Extraction & Model Update
- [ ] Task: Update `Property` TypedDict in `models.py` to include `agency_name` and `agency_phone`
- [ ] Task: Create unit tests for extracting agency info from `__NEXT_DATA__` JSON (TDD - Red)
- [ ] Task: Implement extraction logic in `rightmove_search.py` to pass tests (TDD - Green)
- [ ] Task: Verify extraction works on real/cached data (Manual Verification)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Data Extraction & Model Update' (Protocol in workflow.md)

## Phase 2: Presentation (HTML Dashboard)
- [ ] Task: Update `templates/results.html` to display `agency_name` and `agency_phone` in the Property column
- [ ] Task: Verify HTML dashboard renders correctly with new data (Manual Verification)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Presentation (HTML Dashboard)' (Protocol in workflow.md)
