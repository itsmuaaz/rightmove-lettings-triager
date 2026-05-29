# Specification: Unified TOML Configuration System

## Overview
This feature introduces a unified configuration system utilizing a `config.toml` file in the root of the project. It consolidates all user-configurable parameters—such as API keys, scoring weights, Gemini AI prompt instructions, and work coordinates—into a single, highly readable standard TOML file. By using Python's standard `tomllib` (available in Python 3.11+), we introduce **zero external dependencies**.

## Functional Requirements

### 1. `config.toml` Structure
The configuration file will follow this structure:
```toml
[credentials]
tfl_app_id = ""
tfl_app_key = ""
google_maps_api_key = ""

[commute]
# Latitude/Longitude coordinates for travel destination
work_latitude = 51.5349
work_longitude = -0.1238

[scoring.weights]
price = 0.3
commute = 0.3
vibe = 0.3
freshness = 0.1

[ai]
vibe_prompt_instructions = """
You are a London property market expert.
Analyze the 'vibe' of the following London locations (postcode districts or full addresses)...
"""
```

### 2. Precedence and Merging (API Keys)
- The script will first load settings from `config.toml`.
- Any environment variables set in `.env` (or the shell environment) will **override** the keys in `config.toml`. This ensures that personal secrets do not have to be committed to version control.

### 3. Work Coordinates Migration
- Remove the hardcoded `WORK_LOCATION_COORDS` from `rightmove_search.py` entirely.
- Coordinates must be read dynamically from `config.toml`. If missing or invalid, the script will gracefully error out on startup and instruct the user to set them.

### 4. Scoring Configuration Migration
- Deprecate `.scoring_config.json`.
- When the interactive CLI prompt runs on startup, any user updates to the scoring weights will be written directly back to `config.toml` (under `[scoring.weights]`) using Python's standard library or a simple formatted rewrite block to ensure we do not wipe out comments in `config.toml`.

### 5. Template and Automatic Fallback
- Provide a `config.toml.template` file in the repository.
- If `config.toml` is missing on script startup, automatically copy the template file to `config.toml` and instruct the user to configure it.

## Acceptance Criteria
- [ ] `config.toml` is parsed successfully using Python's native `tomllib` (Python 3.11+).
- [ ] No hardcoded coordinates exist in the Python files; they are successfully read from TOML.
- [ ] CLI prompts write weight updates back to TOML, preserving other sections.
- [ ] `.env` values correctly override `config.toml` credentials.
- [ ] Automated tests verify the new TOML loading, precedence, and parsing logic.

## Out of Scope
- Writing custom TOML serializer from scratch (since Python standard library only has read-only `tomllib`, we can write back changes using a simple and safe line-replacement block to preserve comments, or fallback to simple serialization).