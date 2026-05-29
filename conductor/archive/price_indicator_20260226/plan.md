# Implementation Plan - Relative Price Indicator

## Phase 1: Logic and Data Preparation
- [x] Task: Create `extract_numeric_price` utility function in `utils.py` to parse price strings (TDD - Red/Green)
- [x] Task: Update `generate_report` in `reporter.py` to perform a pre-processing pass to find global min and max prices (TDD - Red/Green)
- [x] Task: Update `_enrich_property` to accept `min_price` and `max_price` and calculate the relative HSL color (Green to Red) (TDD - Red/Green)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Logic and Data Preparation' (Protocol in workflow.md) [checkpoint: c3c0a52]

## Phase 2: UI Integration
- [x] Task: Update `templates/report.html` to render the colored circular marker next to the price (TDD - Red/Green) [842ceaf]
- [x] Task: Ensure code coverage for modified modules remains >80% [842ceaf]
- [x] Task: Conductor - User Manual Verification 'Phase 2: UI Integration' (Protocol in workflow.md) [checkpoint: 842ceaf]

## Phase: Review Fixes
- [x] Task: Apply review suggestions
