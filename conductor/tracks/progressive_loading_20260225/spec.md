# Progressive Results Loading - Specification

## Goal
Enable users to view and interact with all properties immediately upon search completion, with detailed metrics (commute, amenities) populating incrementally as background processing completes.

## User Story
As a user, I want to see the full list of potential properties immediately, even if some details are still loading, so that I can get an overview of the market and start reviewing available information without waiting for the full batch processing.

## Key Features
1.  **Immediate & Incremental Display**:
    -   The dashboard server must start *immediately* after the initial property fetch (Phase 1).
    -   **All fetched properties** must be displayed in the list immediately.
    -   Properties that have not yet been processed (commute/amenity calculations pending) must display **"Loading..." placeholders** or visual indicators for the missing data fields.
    -   Properties that are fully processed must display their complete data (commute times, amenity distances).

2.  **Status Indication**:
    -   A prominent status banner should display: "Processing: X of Y properties completed. [Refresh to update]"
    -   The total count (Y) must be accurate.
    -   The processed count (X) must reflect the current state on page load.

3.  **Sorting Behavior**:
    -   **Dynamic Re-sort:** When the page is refreshed, the list should be re-sorted based on the currently available data (e.g., if sorting by commute time, processed items with short commutes will bubble to the top). Users should be aware that items may move between refreshes.

4.  **Refresh Mechanism**:
    -   **Manual Refresh:** The user must manually refresh the page (browser refresh or a "Refresh Results" button) to see the latest progress and updated sorting. No auto-refresh or polling is required.

## Technical Constraints
-   **Thread Safety:** The `HTTPServer` (reader) and the main processing loop (writer) must access the shared property list safely.
-   **Architecture:** Maintain the current simple architecture (Python script + `http.server` + Jinja2).
-   **State Management:** The application must handle the transition of a property from "raw" to "processed" without data loss.

## Success Metrics
-   **Time to First Result (TTFR):** < 5 seconds (displaying the full list with placeholders).
-   **User Feedback:** Users can identify which properties are still loading versus those that are complete.
