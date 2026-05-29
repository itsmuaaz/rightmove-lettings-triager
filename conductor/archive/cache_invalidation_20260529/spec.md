# Specification - Revamp Cache Invalidation & TTL System

## Overview
This track addresses long-term cache stagnation and storage bloating across both the TfL API client and the Vibe client:
1. **Unexpiring TfL Cache:** Current caching logic does not validate if `arrival_benchmark` is stale. Cycling commutes also have static parameters and never invalidate. This results in frozen, stale commute data.
2. **Unexpiring Vibe Cache:** Vibe scores are cached permanently with no timestamps or expiration limits.
3. **No Storage Cleanup:** Old cached files from past weeks persist indefinitely inside `.tfl_cache/`.
4. **Poor Auditability:** The CLI does not clearly distinguish between cache hits, stale bypasses, and active API fetches.

## Functional Requirements
1. **TfL Cache Expiration & Invalidation:**
   - Update `tfl_client.py:_load_cache` to check the stored `arrival_benchmark` inside the JSON file.
   - If the current time is past the cached `arrival_benchmark`, treat the cache as stale (bypass and delete/overwrite). This guarantees both public transport and cycling commute times refresh naturally week-over-week.
2. **Vibe Cache TTL & Timestamps:**
   - Add `VIBE_CACHE_TTL_DAYS = 30` to `config.py`.
   - Update the `.vibe_cache.json` structure to store entries with a `"cached_at"` ISO timestamp:
     ```json
     {
       "SW14": {
         "score": 8,
         "summary": "Leafy village",
         "cached_at": "2026-05-29T12:00:00"
       }
     }
     ```
   - When loading vibe data, if `"cached_at"` is older than `VIBE_CACHE_TTL_DAYS`, bypass the cached value and re-fetch from Gemini.
   - Handle legacy cache entries gracefully by treating missing `"cached_at"` fields as expired.
3. **Automated Cache Maintenance Chores:**
   - In `rightmove_search.py`, run an automated cache cleanup at the start of every search session.
   - The cleanup chore must scan `.tfl_cache/` and delete any JSON files whose `arrival_benchmark` is in the past.
4. **Improved Audit Logging:**
   - Write cleanly formatted caching events to `sys.stderr` to provide transparency and auditability:
     - `[CACHE HIT] TfL commute from A to B: 15 mins`
     - `[CACHE BYPASS - STALE] TfL benchmark expired. Fetching fresh data...`
     - `[CACHE MISS] No cache for SW14. Querying Gemini...`

## Non-Functional Requirements
- **Performance:** Invalidation checks and cache directory scans must be fast to ensure search start-up remains instantaneous.
- **Robustness:** Gracefully handle legacy, corrupted, or malformed cache files by deleting them rather than crashing.

## Acceptance Criteria
- Running a search session in a new week automatically invalidates old commute and vibe caches, prompting fresh API calls.
- Stale `.tfl_cache` files are successfully scanned and purged at search start-up.
- `sys.stderr` clearly reports cache hits, stale bypasses, and cache misses.
- Test suite verifies cache expiration logic and cleanup routines (with simulated/mocked times and files).

## Out of Scope
- Full refactoring of the Overpass API (OSM) caching system.
- Storing caches in a real database (SQLite).