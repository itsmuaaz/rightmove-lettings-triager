# Implementation Plan - Unified TOML Configuration System

## Phase 1: Config Loader & Migrating Coordinates
- [ ] Task: Create `config.toml.template` with standard default settings and instructions (Chore)
- [ ] Task: Implement TOML loading and merging logic (with `.env` overrides) in `config_manager.py` (TDD - Red/Green)
- [ ] Task: Create unit tests in `tests/test_toml_config.py` to verify config loading, precedence, and default fallbacks (TDD - Red)
- [ ] Task: Update `rightmove_search.py` to use the new TOML config loader and completely remove hardcoded coordinates (Integration)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Config Loader & Migrating Coordinates' (Protocol in workflow.md)

## Phase 2: Weights Migration & Script Integration
- [ ] Task: Implement a robust weight-updating helper in `config_manager.py` that saves weights back to `config.toml` cleanly (TDD - Red/Green)
- [ ] Task: Create unit tests verifying updating weights in TOML works and preserves other sections (TDD - Red)
- [ ] Task: Integrate weight updates into `rightmove_search.py` on startup, deprecating `.scoring_config.json` (Integration)
- [ ] Task: Update `vibe_client.py` to read the Gemini prompt template dynamically from `config.toml` (Integration)
- [ ] Task: Run the entire test suite and verify no regressions in scoring, caching, or execution (Verification)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Weights Migration & Script Integration' (Protocol in workflow.md)