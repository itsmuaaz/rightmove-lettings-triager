# Implementation Plan - Smart Scoring System

## Phase 1: Core Scoring Logic
- [x] Task: Create `get_days_since` utility in `utils.py` [88a3f33]
    - [ ] Sub-task: Write Tests (Ensure accurate day difference calculation and handling of invalid dates)
    - [ ] Sub-task: Implement Feature (Parse ISO strings and return integer days)
- [x] Task: Create `SmartScorer` class in `scoring.py` (New Module) [673c5c6]
    - [ ] Sub-task: Write Tests (Test `calculate_score` with various scenarios: Perfect property, Worst property, Missing data redistribution)
    - [ ] Sub-task: Implement Feature (Weighted sum logic, Normalization helpers, Config usage)
- [x] Task: Externalize Configuration [12f33ae]
    - [ ] Sub-task: Implement Feature (Add `SCORING_WEIGHTS`, `MAX_COMMUTE_MINS`, `FRESHNESS_DECAY_DAYS` to `config.py`)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Core Scoring Logic' (Protocol in workflow.md) [checkpoint: e3828cc]

## Phase 2: Integration & Aggregation
- [x] Task: Refactor `rightmove_search.py` to support two-pass processing [c2b2215]
    - [x] Sub-task: Implement Feature (Pass 1: Fetch & Enrich -> Pass 2: Calculate Global Stats & Score)
    - [x] Sub-task: Write Tests (Verify `min_price` and `max_price` are correctly derived from the full dataset)
- [x] Task: Update Property Data Model [c2b2215]
    - [x] Sub-task: Implement Feature (Inject `smart_score` and `score_breakdown` into the property dictionary)
- [x] Task: Update Sorting Logic [c2b2215]
    - [x] Sub-task: Implement Feature (Update `get_sort_key` or main sort to use `smart_score` descending)
- [x] Task: Conductor - User Manual Verification 'Phase 2: Integration & Aggregation' (Protocol in workflow.md) [checkpoint: 01e879d]

## Phase 3: Dashboard Visualization
- [x] Task: Update `reporter.py` to process the score [ed1b58c]
    - [x] Sub-task: Implement Feature (Add color class logic: Green >90, Yellow >70, etc.)
- [x] Task: Update `templates/report.html` [f548074]
    - [x] Sub-task: Implement Feature (Add Badge UI component with Tooltip showing breakdown)
- [x] Task: Verify Sorting in Dashboard [c2b2215]
    - [x] Sub-task: Manual Verification (Ensure properties appear in the correct order)
- [x] Task: Conductor - User Manual Verification 'Phase 3: Dashboard Visualization' (Protocol in workflow.md) [checkpoint: cabc7aa]

## Phase: Review Fixes
- [~] Task: Apply review suggestions