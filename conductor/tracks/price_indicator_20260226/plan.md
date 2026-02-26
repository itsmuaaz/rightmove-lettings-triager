# Implementation Plan - Relative Price Indicator

## Phase 1: Logic and Data Preparation
- [ ] Task: Create `extract_numeric_price` utility function in `utils.py` to parse price strings (TDD - Red/Green)
- [ ] Task: Update `generate_report` in `reporter.py` to perform a pre-processing pass to find global min and max prices (TDD - Red/Green)
- [ ] Task: Update `_enrich_property` to accept `min_price` and `max_price` and calculate the relative HSL color (Green to Red) (TDD - Red/Green)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Logic and Data Preparation' (Protocol in workflow.md)

## Phase 2: UI Integration
- [ ] Task: Update `templates/report.html` to render the colored circular marker next to the price (TDD - Red/Green)
- [ ] Task: Ensure code coverage for modified modules remains >80%
- [ ] Task: Conductor - User Manual Verification 'Phase 2: UI Integration' (Protocol in workflow.md)