# Implementation Plan - Fix "Added On" Date

## Phase 1: Investigation & Debug
- [x] Task: Create a script `debug_rightmove.py` to fetch a search page and dump the relevant property JSON structure to a file (Manual)
- [x] Task: Analyze the JSON dump to identify the correct date field (e.g., `addedOn`, `listingUpdate.listingUpdateDate`) (Manual)
- [x] Task: Update the `spec.md` with the identified field name (Documentation)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Investigation & Debug' (Protocol in workflow.md)

## Phase 2: Implementation
- [x] Task: Update `parse_property_data` in `rightmove_search.py` to extract the identified date field(s) (TDD - Red/Green)
- [x] Task: Verify and update `utils.format_date` to handle the new date format (TDD - Red/Green)
- [x] Task: Implement fallback logic for missing dates (e.g., fallback to `Unknown`) (TDD - Red/Green)
- [x] Task: Conductor - User Manual Verification 'Phase 2: Implementation' (Protocol in workflow.md) [checkpoint: f1de9e2]

## Phase 3: Bug Fix (User Feedback)
- [x] Task: Update `parse_property_data` to prioritize the most recent date (`max(firstVisibleDate, listingUpdateDate)`) (TDD - Red/Green)
- [x] Task: Verify fix with reported property ID 149322863 (Manual)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Bug Fix' (Protocol in workflow.md)
