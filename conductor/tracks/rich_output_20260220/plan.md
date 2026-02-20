# Implementation Plan - Richer Output Format (Enriched MD & Styled HTML)

This plan outlines the steps to implement a richer reporting system using Markdown and HTML, including property images and color-coded metrics.

---

## Phase 1: Dependency & Data Extraction
- [x] Task: Add `markdown` library to `requirements.txt` and update `tech-stack.md` 7c5611e
- [x] Task: Update property extraction logic to include images, bedrooms, and dates (TDD - Red/Green) d46c1c2
- [x] Task: Implement `FormattedDate` helper for human-readable dates (TDD - Red/Green) d46c1c2
- [x] Task: Conductor - User Manual Verification 'Phase 1: Dependency & Data Extraction' (Protocol in workflow.md) d46c1c2

## Phase 2: Markdown Logic with Color Classes
- [ ] Task: Create `Reporter` class to manage Markdown generation (TDD - Red/Green/Refactor)
- [ ] Task: Implement `get_commute_class` and similar helpers for visual cues (TDD - Red/Green)
- [ ] Task: Refactor `main()` to use the `Reporter` and save `results.md`
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Markdown Logic with Color Classes' (Protocol in workflow.md)

## Phase 3: HTML Conversion & Styling
- [ ] Task: Create HTML boilerplate with embedded CSS for the traffic light system
- [ ] Task: Implement MD-to-HTML conversion logic using `markdown.markdown()` (TDD - Red/Green)
- [ ] Task: Integrate HTML generation into the final script execution flow
- [ ] Task: Verify the end-to-end flow and visual rendering in browser
- [ ] Task: Ensure code coverage for new modules is >80%
- [ ] Task: Conductor - User Manual Verification 'Phase 3: HTML Conversion & Styling' (Protocol in workflow.md)
