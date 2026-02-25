# Implementation Plan - Commute Cost Integration

## Phase 1: TfL Client & Data Model Enhancement [checkpoint: 4125d8b]
- [x] Task: Update `TflClient` to extract fare information (peak/off-peak) from the Journey Planner API response (TDD - Red Phase) [8c12a1b]
- [x] Task: Implement fare extraction logic in `TflClient._parse_journey_response` or similar (TDD - Green Phase) [8c12a1b]
- [x] Task: Update the `TflClient` caching mechanism to include a `fares` field in the stored JSON (TDD - Green/Refactor) [8c12a1b]
- [x] Task: Conductor - User Manual Verification 'Phase 1: TfL Client & Data Model Enhancement' (Protocol in workflow.md) [4125d8b]

## Phase 2: Commute Calculator & Data Propagation [checkpoint: 25f5bf3]
- [x] Task: Update `CommuteCalculator` to include fare data in the result dictionary returned by `calculate` (TDD - Red Phase) [3eabed3]
- [x] Task: Implement the propagation of fare data from `TflClient` through `CommuteCalculator` (TDD - Green Phase) [3eabed3]
- [x] Task: Ensure the `rightmove_search.py` processing loop correctly handles the updated result structure (Refactor) [3eabed3]
- [x] Task: Conductor - User Manual Verification 'Phase 2: Commute Calculator & Data Propagation' (Protocol in workflow.md) [25f5bf3]

## Phase 3: Dashboard UI Update (Jinja2) [checkpoint: 0b14301]
- [x] Task: Update `reporter.py` to pass the peak and off-peak fares to the template (TDD - Red Phase) [105fede]
- [x] Task: Modify the `templates/report.html` (or the commute badge macro) to display the cost inline with the time (TDD - Green Phase) [105fede]
- [x] Task: Implement CSS styling for the cost text to ensure it is readable but secondary to the duration (Style) [105fede]
- [x] Task: Conductor - User Manual Verification 'Phase 3: Dashboard UI Update (Jinja2)' (Protocol in workflow.md) [0b14301]

## Phase 4: Verification & Cache Migration [checkpoint: 5219cf3]
- [x] Task: Verify the full flow with a real search and ensure costs are displayed and cached (Manual) [0b14301]
- [x] Task: (Optional) Create a migration script or handle missing fare data in the existing cache gracefully (Chore) [0b14301]
- [x] Task: Conductor - User Manual Verification 'Phase 4: Verification & Cache Migration' (Protocol in workflow.md) [5219cf3]