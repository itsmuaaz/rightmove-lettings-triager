# Implementation Plan - Commute Navigation Links

This plan outlines the steps to generate and display navigation links for properties.

## Phase 1: URL Generation Logic
- [ ] Task: Create a new utility function for generating navigation URLs (add to `utils.py`).
    -   Define constants for Work Address and Coordinates.
- [ ] Task: Implement `generate_google_maps_url(origin_address)` (TDD - Red/Green).
- [ ] Task: Implement `generate_tfl_url(origin_address, origin_coords)` (TDD - Red/Green).
- [ ] Task: Verify URLs with unit tests, checking for correct query parameters and encoding.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: URL Generation Logic' (Protocol in workflow.md)

## Phase 2: Reporter Integration
- [ ] Task: Update `Reporter` class in `reporter.py` to incorporate the new link generator functions.
- [ ] Task: Modify `_generate_commute_cell` to append `[GMaps]` and `[TfL]` links.
    -   Ensure links are added to both Markdown (inline) and HTML (styled) outputs.
- [ ] Task: Verify the visual output in `results.md` and `results.html` matches the specification.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Reporter Integration' (Protocol in workflow.md)
