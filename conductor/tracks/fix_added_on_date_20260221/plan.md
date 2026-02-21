# Implementation Plan - Fix "Added On" Date

## Phase 1: Investigation & Debug
- [ ] Task: Create a script `debug_rightmove.py` to fetch a search page and dump the relevant property JSON structure to a file (Manual)
- [ ] Task: Analyze the JSON dump to identify the correct date field (e.g., `addedOn`, `listingUpdate.listingUpdateDate`) (Manual)
- [ ] Task: Update the `spec.md` with the identified field name (Documentation)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Investigation & Debug' (Protocol in workflow.md)

## Phase 2: Implementation
- [ ] Task: Update `parse_property_data` in `rightmove_search.py` to extract the identified date field(s) (TDD - Red/Green)
- [ ] Task: Verify and update `utils.format_date` to handle the new date format (TDD - Red/Green)
- [ ] Task: Implement fallback logic for missing dates (e.g., fallback to `Unknown`) (TDD - Red/Green)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Implementation' (Protocol in workflow.md)
