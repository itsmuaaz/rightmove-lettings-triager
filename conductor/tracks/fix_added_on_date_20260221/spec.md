# Specification: Fix "Added On" Date

## Overview
The "Added On" column currently displays "Unknown" for all properties. This track aims to identify the correct data field in the Rightmove response and update the parser to display the correct listing date.

## Functional Requirements

### 1. Data Analysis
- Inspect the raw JSON structure from Rightmove to identify the correct field for the listing date.
- Confirmed field: `firstVisibleDate` (e.g., "2026-01-22T09:06:28Z").
- Secondary field: `listingUpdate.listingUpdateDate` (e.g., "2026-02-19T15:50:34Z") or `addedOrReduced` string.

### 2. Parser Update
- Update `parse_property_data` in `rightmove_search.py` to extract the identified date field.
- Implement fallback logic if the primary field is missing (e.g., try `listingUpdateDate` if `addedOn` is null).

### 3. Formatter Update
- Ensure `utils.format_date` correctly parses the date format returned by the new field (e.g., ISO 8601, DD/MM/YYYY).

### 4. Failure Handling
- If the date cannot be parsed, display "Unknown".
- (Optional) If no date field is reliably found across all properties, consider removing the column (to be decided during implementation).

## Out of Scope
- Changing the overall report layout (unless removing the column).
