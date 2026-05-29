# Specification: User-Configurable Score Breakdown

## Overview
This feature allows users to customize the weights used in the "Smart Scoring System" (Price, Commute, Vibe, Freshness) via an interactive prompt at startup. It supports persistence, so users don't have to re-enter their preferences every time.

## Functional Requirements

### 1. Interactive Configuration
- **Startup Prompt:** When the script runs, it should check for saved preferences.
- **Flow:**
    1.  Load existing weights (or new defaults).
    2.  Display current weights to the user.
    3.  Ask: "Do you want to change these scoring weights? (y/n)"
    4.  If 'y', prompt for new values for each component (Price, Commute, Vibe, Freshness).
- **Defaults:** Update the system defaults to:
    -   Price: 30%
    -   Commute: 30%
    -   Vibe: 30%
    -   Freshness: 10%

### 2. Validation & Normalization
- **Auto-Normalization:** The system must accept raw integer inputs (e.g., 50, 50, 50, 50) and automatically normalize them to sum to 100% (e.g., 25% each).
- **Input Handling:** Gracefully handle non-numeric input (re-prompt or fall back to default).

### 3. Persistence
- **Storage:** Save the user's custom weights to a JSON file (e.g., `.scoring_config.json`) in the project root.
- **Loading:** On startup, prioritize values from `.scoring_config.json` over the hardcoded defaults in `config.py`.

### 4. Integration
- **Scoring Engine:** Ensure the `SmartScorer` class uses the loaded (and potentially normalized) weights instead of just `config.SCORING_WEIGHTS`.

## Non-Functional Requirements
- **UX:** The prompt must be clear and unobtrusive. It should default to "No" (keep current) if the user just hits Enter.
- **Robustness:** If the config file is corrupted, fallback to hardcoded defaults without crashing.

## Out of Scope
- CLI flags for one-off overrides (e.g., `--weights`). This track focuses on the interactive persistent workflow.