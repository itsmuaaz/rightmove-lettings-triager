# Implementation Plan - Unified TOML Configuration System

## Phase 1: Config Loader & Migrating Coordinates
- [x] Task: Create `config.toml.template` with standard default settings and instructions (Chore) [d4db881]
- [x] Task: Implement TOML loading and merging logic (with `.env` overrides) in `config_manager.py` (TDD - Red/Green) [40ab485]
- [x] Task: Create unit tests in `tests/test_toml_config.py` to verify config loading, precedence, and default fallbacks (TDD - Red) [40ab485]
- [x] Task: Update `rightmove_search.py` to use the new TOML config loader and completely remove hardcoded coordinates (Integration) [4d6f147]
- [x] Task: Conductor - User Manual Verification 'Phase 1: Config Loader & Migrating Coordinates' (Protocol in workflow.md) [checkpoint: 0b67a31]

## Phase 2: Weights Migration & Script Integration
- [x] Task: Implement a robust weight-updating helper in `config_manager.py` that saves weights back to `config.toml` cleanly (TDD - Red/Green) [a89e92d]
- [x] Task: Create unit tests verifying updating weights in TOML works and preserves other sections (TDD - Red) [a89e92d]
- [x] Task: Integrate weight updates into `rightmove_search.py` on startup, deprecating `.scoring_config.json` (Integration) [2d6af59]
- [x] Task: Update `vibe_client.py` to read the Gemini prompt template dynamically from `config.toml` (Integration) [2d6af59]
- [x] Task: Run the entire test suite and verify no regressions in scoring, caching, or execution (Verification) [2d6af59]
- [x] Task: Conductor - User Manual Verification 'Phase 2: Weights Migration & Script Integration' (Protocol in workflow.md) [checkpoint: 2d6af59]