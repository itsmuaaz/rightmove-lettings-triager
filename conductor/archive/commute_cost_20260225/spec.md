# Specification: Commute Cost Integration

## Overview
Enhance the commute time display to include the estimated cost of the journey via public transport. This information will be retrieved from the TfL API and displayed inline with the commute duration in the dashboard, providing users with a clearer picture of their daily travel expenses.

## Functional Requirements

### 1. Data Retrieval (TfL API)
- Update the `TflClient` to extract fare/cost information from the journey results returned by the TfL Journey Planner API.
- Capture both Peak and Off-Peak single fares when available to provide a comprehensive cost range.

### 2. Logic & Calculation
- Store the retrieved cost data (min/max fares) within the property data structure.
- Ensure the `CommuteCalculator` correctly handles cases where fare data is missing or incomplete.

### 3. Dashboard UI Update
- Update the commute cell in the HTML dashboard to display the cost inline with the public transport time.
- **Format:** `[Duration] mins (£[Peak] / £[Off-Peak])` or similar.
- If both peak and off-peak are available, show both (e.g., "£3.40 / £2.80").
- Use "N/A" or "Unknown" as a fallback if the cost cannot be determined.

### 4. Caching & Persistence
- Update the `.tfl_cache` structure to include fare data so that costs are not re-fetched unnecessarily.
- Ensure that existing cached entries without fare data are handled gracefully (e.g., by re-fetching on the next run or showing N/A until refreshed).

## Non-Functional Requirements
- **Performance:** Cost retrieval should be bundled with the existing journey planner calls to avoid extra API requests.
- **Simplicity:** The UI remains clean and focuses on providing the cost as a quick-reference metric.

## Acceptance Criteria
- [ ] TfL commute badges in the dashboard show a cost range or single price next to the time.
- [ ] Properties with no public transport commute (e.g., walking only) do not show a cost.
- [ ] The `TflClient` tests are updated to verify fare extraction.
- [ ] The dashboard correctly displays "N/A" if the API returns no fare data.

## Out of Scope
- Calculating weekly or monthly cap totals (this track focus is on single journey cost).
- Cost estimation for cycling or driving.
- Zone-to-zone manual heuristics (rely strictly on TfL API data).