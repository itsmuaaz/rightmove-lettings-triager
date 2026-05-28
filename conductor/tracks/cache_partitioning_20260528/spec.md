# Specification: Cache Partitioning & Targeted Threading

## Overview
This feature introduces a pre-processing "Cache Partitioning" step before the main multi-threaded loop starts. The goal is to identify properties that are already fully cached (possessing commute times, amenities, and vibe scores in their local caches) and process them instantly on the main thread. This completely bypasses the ThreadPoolExecutor for fully cached properties, dramatically reducing startup overhead and ending the script instantly if 100% of properties are already cached.

## Functional Requirements
1. **Cache Detection Pass:**
   - Before launching the `ThreadPoolExecutor`, iterate through all scraped properties.
   - For each property, check if its TfL commute data (Transit and Cycling), OpenStreetMap amenities, and Gemini Vibe score already exist in the local cache files (`.tfl_cache`, `.amenity_cache`, and `.vibe_cache.json`).
2. **Synchronous Processing (Main Thread):**
   - Any property that is determined to be **fully cached** is processed instantly on the main thread.
   - Populating cached data should happen in milliseconds with zero thread overhead.
   - Once all synchronous properties are loaded, perform a single bulk update to the `search_state.processed` progress counter.
3. **Targeted Thread Pool (Targeted Threading):**
   - Only properties that are **missing any cache data** (partially cached or un-cached) are submitted to the `ThreadPoolExecutor` workers.
   - If all properties are fully cached, the ThreadPoolExecutor is completely bypassed.
4. **Dashboard Server Integrity:**
   - Even if 100% of properties are cached and the script finishes processing instantly, the dashboard server must still spin up and run as normal so the user can interact with the results.

## Acceptance Criteria
- [ ] Fully cached properties are processed immediately on startup without being submitted to the ThreadPoolExecutor.
- [ ] If 100% of properties are cached, the multi-threaded processing loop is skipped entirely, and the script instantly enters "Processing Complete" server mode.
- [ ] The dashboard progress counter (`search_state.processed`) reflects the bulk-loaded synchronous properties accurately.
- [ ] Automated tests verify the partitioning logic and ensure there are no regressions in property scoring or sorting.

## Out of Scope
- Modifying the underlying JSON structure of the caches.
- Multi-threaded pre-fetching of missing caches in the main thread (un-cached items are handled inside the thread pool as usual).