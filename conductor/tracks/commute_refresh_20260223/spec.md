# Specification - Commute Stability & Force Refresh

## Overview
Improve the reliability and transparency of commute data by standardizing calculations to a "House-Hunter's Benchmark" (Next Tuesday at 9:00 AM) and providing manual refresh controls in the dashboard.

## Functional Requirements
1. **Standardized Commute Benchmark:**
    - All TfL commute calculations (Public Transport) must use an `ArrivingBy` time of **Upcoming Tuesday at 09:00 AM**.
    - If today is Tuesday before 09:00 AM, use today. Otherwise, use the following Tuesday.
2. **Metadata-Wrapped Caching:**
    - The `TflClient` cache format must be updated to include metadata:
        - `calculated_at`: ISO timestamp of the API call.
        - `arrival_benchmark`: The arrival time used (e.g., "Next Tue 09:00").
        - `response`: The raw TfL API response.
    - Existing legacy cache files in `.tfl_cache/` will be reset (deleted) upon implementation to avoid format conflicts.
3. **Force Refresh Mechanism:**
    - Add a `/api/refresh` POST endpoint to the dashboard server.
    - Support both per-property refresh and a global "Refresh All" action.
    - The refresh logic must bypass the file cache but strictly respect the TfL rate-limiting interval (1.5s).
4. **UI/UX Enhancements:**
    - **Timestamp Display:** Show the absolute "Last Updated" timestamp (e.g., "Updated: 14:30") near the commute badges.
    - **Refresh Icons:** Add a 🔄 button to each property card for individual re-calculation.
    - **Global Action:** Add a "Refresh All Commute Data" button to the dashboard header.
    - **Loading States:** Provide visual feedback (spinners/opacity change) while a refresh is in progress.

## Acceptance Criteria
- [ ] TfL API calls include `date`, `time`, and `timeIs=Arriving` parameters for the benchmark.
- [ ] Dashboard displays the calculation timestamp for each property.
- [ ] Clicking 'Refresh' on a property updates its commute time and timestamp without a full page reload.
- [ ] 'Refresh All' updates all properties sequentially, respecting rate limits.
- [ ] New cache files contain the required metadata structure.

## Out of Scope
- Configurable benchmark times (staying with Tuesday 9:00 AM for now).
- Historical tracking of commute time changes (only the latest calculation is kept).
