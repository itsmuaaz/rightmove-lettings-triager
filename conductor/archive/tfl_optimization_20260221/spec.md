# Specification: TfL Client Optimization

## Overview
The current TfL client lacks rate limiting and caching, leading to HTTP 429 throttling errors when processing large datasets (>200 properties) with concurrency. This track aims to implement robust caching and rate limiting to ensure reliability.

## Functional Requirements

### 1. Caching
- **Storage:** Persist API responses to disk (JSON files).
- **Location:** `.tfl_cache/` directory.
- **Keying:** Unique hash based on origin, destination, and query parameters.
- **Behavior:**
    - On request: Check cache. If hit, return data immediately.
    - On miss: Fetch from API, then save to cache.

### 2. Rate Limiting
- **Mechanism:** Thread-safe interval enforcement.
- **Limit:** Max 1 request every 1.5 seconds (approx 40 req/min, safe buffer under the 50 limit).
- **Behavior:** Block (sleep) the calling thread until the time slot is available.

### 3. Error Handling
- **429 Handling:** If a 429 occurs despite rate limiting, backoff aggressively (e.g., 10-30 seconds) before retrying.

## Non-Functional Requirements
- **Thread Safety:** The rate limiter must work correctly when called from multiple threads (`ThreadPoolExecutor`).
- **Transparency:** The caller (`CommuteCalculator`) should not need changes; improvements should be encapsulated within `TflClient`.

## Out of Scope
- Changing the concurrency model of the main script (though the rate limiter will naturally throttle it).
- In-memory caching (disk is preferred for cross-run persistence).
