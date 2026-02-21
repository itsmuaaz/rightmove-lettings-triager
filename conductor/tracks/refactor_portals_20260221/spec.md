# Specification: Multi-Portal Architecture Refactor

## Overview
Refactor the existing codebase to decouple Rightmove-specific logic and introduce a flexible architecture capable of supporting multiple property portals (e.g., Zoopla, Spareroom) in the future.

## Functional Requirements

### 1. Generic Data Model
- Define a standard `Property` schema (TypedDict or DataClass) to be used across the application.
- **Fields:** `id` (string), `source` (string), `url` (absolute), `price`, `address`, `latitude`, `longitude`, `image_url`, `bedrooms`, `published_on`, `description`.

### 2. Portal Abstraction Layer
- Create a `portals/` package.
- Define an abstract base class `PropertySource` in `portals/base.py`.
- **Interface Methods:**
  - `search(url: str) -> Iterator[Property]`
  - `parse(html: str) -> List[Property]`

### 3. Rightmove Implementation
- Extract scraping logic from `rightmove_search.py` into `portals/rightmove.py`.
- Implement `RightmoveClient` inheriting from `PropertySource`.

### 4. Generic Components
- **CommuteCalculator:** Update `calculate()` to accept standardized `latitude` and `longitude` instead of raw API responses.
- **Reporter:** Update to handle absolute URLs and remove hardcoded `rightmove.co.uk` prefixes.

### 5. Generic Entry Point
- Rename `rightmove_search.py` to `search.py`.
- Implement a factory function `get_client(url: str) -> PropertySource` to select the correct client based on the input URL domain.

## Non-Functional Requirements
- **No Regression:** The functionality for Rightmove searches must remain unchanged. `results.md` and `results.html` should be structurally identical to the current output.
- **Extensibility:** Adding a new portal should only require creating a new file in `portals/` and registering it in the factory.

## Out of Scope
- Implementing support for Zoopla, Spareroom, or other portals (this track is strictly for refactoring).
