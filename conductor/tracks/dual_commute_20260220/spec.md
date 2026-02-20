# Specification: Dual Commute Mode Display (Public Transport & Cycling)

## Overview
Enhance the existing "Commute" column in both the Markdown and HTML reports to display commute times for *two* modes of transport: Public Transport (existing) and Cycling (new). Both values will be fetched from the TfL Unified API. The system will color-code both times independently and sort the final results based on the shorter of the two durations.

## Functional Requirements

### 1. Data Fetching
- **Source:** Fetch journey times for both "Public Transport" and "Cycling" from the TfL API.
- **Cycling Preference:** Use a "Moderate" cycle preference (e.g., `cyclePreference=allTheWay` or similar balanced option).
- **Error Handling:** 
    - If one mode fails, display "N/A" for that mode but show the successful one.
    - If both fail, display "N/A" for the cell (or fallback to straight-line distance if applicable).

### 2. Data Processing
- **Calculation:** Retrieve duration (minutes) for both modes for every property.
- **Sorting:** Sort the final property list based on the **minimum** of the two available times (e.g., `min(public_time, cycling_time)`).

### 3. Markdown Reporting (`results.md`)
- **Format:** Display values inline with icons, separated by a slash.
- **Example:** `[Green Badge] 20m 🚆 / [Green Badge] 15m 🚲`
- **Styling:** Apply existing traffic light logic (Green < 20m, Amber 20-40m, Red > 40m) to *each* value independently.

### 4. HTML Reporting (`results.html`)
- **Layout:** Stack the two values vertically within the "Commute" table cell.
- **Styling:** 
    - Use a flexbox or block layout to stack the badges.
    - Ensure consistent spacing and alignment.
    - Example:
      ```html
      <div class="commute-stack">
        <span class="badge badge-green">20m 🚆</span>
        <span class="badge badge-green">15m 🚲</span>
      </div>
      ```

## Non-Functional Requirements
- **Performance:** Ensure API rate limits are respected with the increased number of calls (potential 2x calls per property).
- **Resilience:** The application must continue processing other properties even if one property's data fetch fails completely.

## Acceptance Criteria
- [ ] `results.md` shows both Public Transport and Cycling times with icons.
- [ ] `results.html` shows both times stacked vertically.
- [ ] Cycling times are accurate according to TfL API "Moderate" settings.
- [ ] Both times have independent color-coded badges (Green/Amber/Red).
- [ ] The results list is sorted by the shortest commute option.
