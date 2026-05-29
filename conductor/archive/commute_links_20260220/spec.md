# Specification: Commute Navigation Links Integration

## Overview
Add direct navigation links to Google Maps and the TfL Journey Planner within the "Commute" section of the property reports. These links will allow the user to immediately view the route from the specific property to their fixed work location.

## Functional Requirements

### 1. Link Generation
- **Work Location:**
    -   **Address:** "6 Pancras Square, N1C 4AG"
    -   **Coordinates:** (51.5349, -0.1238)
- **Google Maps Link:**
    -   **Format:** `https://www.google.com/maps/dir/?api=1&origin={Prop_Address}&destination={Work_Address}&travelmode=transit` (or similar robust format).
    -   **Mode:** Public Transport.
- **TfL Journey Planner Link:**
    -   **Format:** `https://tfl.gov.uk/plan-a-journey/results?InputFrom={Prop_Address}&FromId={Prop_Coords}&InputTo={Work_Address}&ToId={Work_Coords}`
    -   **Inputs:** URL-encoded addresses and coordinates.

### 2. Report Integration
- **Column:** Add to the existing "Commute" column.
- **Link Text:** Display as `[GMaps]` and `[TfL]`.
- **Layout:**
    -   **Markdown:** Appended to the commute times, separated by a space or line break (e.g., `20m 🚆 [GMaps] [TfL]`).
    -   **HTML:** Displayed clearly, possibly on a new line below the badges for better readability.

## Non-Functional Requirements
- **Robustness:** Ensure proper URL encoding for all address parameters to prevent broken links.
- **Fallback:** If property coordinates are missing, generate links using only the address.

## Acceptance Criteria
- [ ] `results.md` includes working `[GMaps]` and `[TfL]` links in the Commute column.
- [ ] `results.html` includes working `[GMaps]` and `[TfL]` links in the Commute cell.
- [ ] Google Maps link correctly pre-fills Origin, Destination (6 Pancras Sq), and Mode (Transit).
- [ ] TfL link correctly pre-fills Origin (with coords if avail) and Destination (with coords).
