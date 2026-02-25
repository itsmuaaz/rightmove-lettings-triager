# Implementation Plan - Commute Cost Integration

## Phase 1: TfL Client & Data Model Enhancement
- [x] Task: Update `TflClient` to extract fare information (peak/off-peak) from the Journey Planner API response (TDD - Red Phase) [8c12a1b]
- [x] Task: Implement fare extraction logic in `TflClient._parse_journey_response` or similar (TDD - Green Phase) [8c12a1b]
- [x] Task: Update the `TflClient` caching mechanism to include a `fares` field in the stored JSON (TDD - Green/Refactor) [8c12a1b]
- [ ] Task: Conductor - User Manual Verification 'Phase 1: TfL Client & Data Model Enhancement' (Protocol in workflow.md)

## Phase 2: Commute Calculator & Data Propagation
- [ ] Task: Update `CommuteCalculator` to include fare data in the result dictionary returned by `calculate` (TDD - Red Phase)
- [ ] Task: Implement the propagation of fare data from `TflClient` through `CommuteCalculator` (TDD - Green Phase)
- [ ] Task: Ensure the `rightmove_search.py` processing loop correctly handles the updated result structure (Refactor)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Commute Calculator & Data Propagation' (Protocol in workflow.md)

## Phase 3: Dashboard UI Update (Jinja2)
- [ ] Task: Update `reporter.py` to pass the peak and off-peak fares to the template (TDD - Red Phase)
- [ ] Task: Modify the `templates/report.html` (or the commute badge macro) to display the cost inline with the time (TDD - Green Phase)
- [ ] Task: Implement CSS styling for the cost text to ensure it is readable but secondary to the duration (Style)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Dashboard UI Update' (Protocol in workflow.md)

## Phase 4: Verification & Cache Migration
- [ ] Task: Verify the full flow with a real search and ensure costs are displayed and cached (Manual)
- [ ] Task: (Optional) Create a migration script or handle missing fare data in the existing cache gracefully (Chore)
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Verification & Cache Migration' (Protocol in workflow.md)