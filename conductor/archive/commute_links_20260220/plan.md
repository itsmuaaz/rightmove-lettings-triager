# Implementation Plan - Commute Navigation Links

This plan outlines the steps to generate and display navigation links for properties.

## Phase 1: URL Generation Logic [checkpoint: 24f63b2]
- [x] Task: Create a new utility function for generating navigation URLs (add to `utils.py`). f075b03
    -   Define constants for Work Address and Coordinates.
- [x] Task: Implement `generate_google_maps_url(origin_address)` (TDD - Red/Green). f075b03
- [x] Task: Implement `generate_tfl_url(origin_address, origin_coords)` (TDD - Red/Green). f075b03
- [x] Task: Verify URLs with unit tests, checking for correct query parameters and encoding. f075b03
- [x] Task: Conductor - User Manual Verification 'Phase 1: URL Generation Logic' (Protocol in workflow.md) 24f63b2

## Phase 2: Reporter Integration [checkpoint: f7d6bee]
- [x] Task: Update `Reporter` class in `reporter.py` to incorporate the new link generator functions. 170544b
- [x] Task: Modify `_generate_commute_cell` to append `[GMaps]` and `[TfL]` links. 170544b
    -   Ensure links are added to both Markdown (inline) and HTML (styled) outputs.
- [x] Task: Verify the visual output in `results.md` and `results.html` matches the specification. 170544b
- [x] Task: Conductor - User Manual Verification 'Phase 2: Reporter Integration' (Protocol in workflow.md) f7d6bee

## Phase: Review Fixes
- [x] Task: Apply review suggestions (CSS refactor) 398aecb
