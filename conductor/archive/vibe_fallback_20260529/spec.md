# Specification - Fix Vibe Scoring & Address Fallback

## Overview
This track fixes two critical bugs in the UK Letting Researcher tool:
1. **Persistent `N/A` Vibe Scores:** Occurs when Rightmove's `displayAddress` is a property description (e.g., `"2 bedroom flat"`) rather than a geographical location. This prevents the Gemini API from parsing and returning a vibe score, resulting in a permanent `N/A` value in the report.
2. **Vibe Client Thread Safety:** When running `rightmove_search.py` with concurrent threads, multiple workers concurrently fetch vibes and write to `.vibe_cache.json` without a lock, causing write collisions and missing cache keys.

## Functional Requirements
1. **Reverse-Geocoding Fallback via `postcodes.io`:**
   - When extracting the postcode district from a property address in `utils.py`, if no postcode district is found (e.g., when the address contains descriptions like `"2 bedroom flat"`), the system must fallback to reverse-geocoding using the property's `latitude` and `longitude`.
   - Perform a `GET` request to `https://api.postcodes.io/postcodes?lon={longitude}&lat={latitude}` with a 3-second timeout (`Fail Fast`).
   - If the request is successful, extract the `outcode` (e.g., `"WC2N"`) from the first result and use it as the postcode district.
   - If geocoding fails, times out, or returns no results, gracefully fall back to `None` immediately.
2. **Geocode Caching:**
   - To avoid duplicate web requests for identical coordinates, implement local caching for geocoding results (coordinates map to the geocoded postcode district) in-memory during the execution session.
3. **Thread-Safe Vibe Caching:**
   - Implement a `threading.Lock` inside the `VibeClient` to synchronize thread access.
   - Use the lock to guard both in-memory cache updates (`self.cache` dictionary manipulation) and the disk write operation (`self._save_cache()`).

## Non-Functional Requirements
- **Performance:** Geocoding calls must use a 3-second timeout to prevent the scraping script from hanging.
- **Thread Safety:** Ensure zero file lock contention or race conditions when writing to `.vibe_cache.json`.

## Acceptance Criteria
- Properties with addresses like `"2 bedroom flat"` must successfully resolve to their correct postcode district using coordinates and retrieve a non-`N/A` vibe score from Gemini.
- All 40/40 properties should consistently have valid vibe scores if coordinates are available.
- Concurrent processing must not raise file write errors, corrupted cache reads, or race conditions.
- Extensive test coverage (>80%) for new reverse-geocoding and thread-safe vibe caching modules.

## Out of Scope
- Interacting with Google Maps API for geocoding (use `postcodes.io` only).
- Refactoring the entire scraping pipeline.