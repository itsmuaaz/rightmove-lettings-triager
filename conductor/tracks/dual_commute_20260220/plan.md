# Implementation Plan - Dual Commute Mode Display

This plan outlines the steps to integrate Cycling commute times alongside Public Transport times in the search results.

## Phase 1: TfL Client Enhancement [checkpoint: 1c2cc4f]
- [x] Task: Research TfL API documentation for Cycling options (`cyclePreference`) to determine correct query parameters. 4a9aefe

- [x] Task: Update `TflClient` to support fetching cycling journey times (TDD - Red/Green). 43c3240

    - Add `mode` parameter to `get_commute_time` or create `get_cycling_time`.
    - Implement logic for "Moderate" cycle preference.
- [x] Task: Verify updated client with unit tests covering both modes and error scenarios. 6e46269

- [x] Task: Conductor - User Manual Verification 'Phase 1: TfL Client Enhancement' (Protocol in workflow.md) 1c2cc4f

## Phase 2: Data Processing & Integration [checkpoint: 3f9a6be]
- [x] Task: Update `main` loop in `rightmove_search.py` to fetch both Public Transport and Cycling times for each property. c645dbe
- [x] Task: Implement error handling logic: ensure failure in one mode doesn't block the other (TDD - Red/Green). c645dbe
- [x] Task: Update sorting logic to sort properties by the *minimum* of the two available commute times (TDD - Red/Green). f8c272f
- [x] Task: Conductor - User Manual Verification 'Phase 2: Data Processing & Integration' (Protocol in workflow.md) 3f9a6be


## Phase 3: Reporting Updates
- [x] Task: Update `Reporter` class to accept two commute values per property (TDD - Red/Green). ac58312
- [x] Task: Implement `_generate_commute_cell_md` helper for the new inline format with icons (`🚆 / 🚲`) (TDD - Red/Green). ac58312
- [x] Task: Implement `_generate_commute_cell_html` helper for the new stacked format (TDD - Red/Green). ac58312
- [x] Task: Update CSS in `get_html_template` to support `.commute-stack` class for vertical alignment. ac58312
- [x] Task: Verify the visual output in `results.md` and `results.html` matches the specification. ac58312
- [x] Task: Conductor - User Manual Verification 'Phase 3: Reporting Updates' (Protocol in workflow.md) f310a32
