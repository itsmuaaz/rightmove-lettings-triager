# Design Document: TfL Client Optimization

## 1. Problem Statement
The current implementation of `rightmove_search.py` processes properties concurrently (3 workers), and for each property, it fetches public transport and cycling times in parallel (2 requests). This results in a burst of up to 6 concurrent requests. For a dataset of 200+ properties (400+ requests), this rapidly exhausts the TfL API rate limit of 50 requests/minute, resulting in HTTP 429 errors and data loss.

## 2. Proposed Solution
To improve resilience and respect API limits, we will implement a two-pronged approach within `TflClient`:
1.  **Persistent Caching:** Store API responses on disk to avoid redundant network calls.
2.  **Rate Limiting:** Enforce a strict request interval to ensure compliance with the 50 req/min limit.

## 3. Detailed Design

### 3.1 Caching Strategy
-   **Storage:** JSON files in a hidden directory `.tfl_cache/`.
-   **Key Generation:** SHA256 hash of: `f"{origin_lat},{origin_lon}|{dest_lat},{dest_lon}|{sorted_params}"`.
-   **Logic:**
    -   Before request: Check if valid cache file exists. If yes, return data.
    -   After success: Write data to cache file.
-   **TTL:** Optional, but for now we assume journey times are stable enough to cache indefinitely or until manual clear.

### 3.2 Rate Limiting
-   **Mechanism:** Thread-safe "Leaky Bucket" or simple "Minimum Interval" enforcement.
-   **Interval:** 50 req/min = ~1.2 seconds per request. To be safe, we will use **1.5 seconds**.
-   **Implementation:**
    -   Shared `threading.Lock` and `last_request_time` timestamp.
    -   Before making a request (if cache miss), acquire lock.
    -   Calculate wait time: `max(0, 1.5 - (now - last_request_time))`.
    -   Sleep.
    -   Update `last_request_time`.
    -   Release lock.
    -   Execute request.

### 3.3 Retry Logic Update
-   Update `_fetch_journey` to explicitly handle HTTP 429.
-   If 429 received: Sleep for a longer duration (e.g., 10s) and retry, regardless of the local rate limiter (as we might be out of sync with the server's bucket).

## 4. Implementation Plan (Track: tfl_optimization)

### Phase 1: Caching
-   [ ] Task: Implement `_get_cache_key` and file handling in `TflClient`.
-   [ ] Task: Update `_fetch_journey` to read/write cache.
-   [ ] Task: Add tests for caching behavior.

### Phase 2: Rate Limiting
-   [ ] Task: Implement thread-safe rate limiting in `TflClient`.
-   [ ] Task: Update `_fetch_journey` to respect the limit.
-   [ ] Task: Verify with 200+ property simulation (mocked network).

## 5. Benefits
-   **Resilience:** Virtually eliminates 429 errors.
-   **Performance:** Subsequent runs will be near-instantaneous due to caching.
-   **Scalability:** Allows processing larger datasets without crashing.
