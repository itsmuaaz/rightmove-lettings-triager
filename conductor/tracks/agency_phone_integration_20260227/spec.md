# Specification: Add Agency Name and Phone Number

## Overview
This feature aims to extract the **Agency Name** (e.g., "OpenRent") and **Phone Number** from Rightmove property listings and display this information in the **HTML Dashboard**.

## Functional Requirements
1.  **Data Extraction:**
    -   Modify the scraping logic to extract `brandTradingName` (Agency Name) and `contactTelephone` (Phone Number) from the `__NEXT_DATA__` JSON blob on the Rightmove search page.
    -   Handle cases where the branch name (e.g., "OpenRent, London") differs from the brand name, preferring the most descriptive one available (e.g., `branchDisplayName`).
2.  **Data Storage:**
    -   Update the `Property` model/schema to include `agency_name` and `agency_phone` fields.
    -   Persist this data in the `history.json` file.
3.  **Presentation (HTML Dashboard):**
    -   Update the HTML template (`results.html`) to display the Agency Name and Phone Number.
    -   **Location:** Append this information to the existing **"Property"** column/section for each listing.
    -   **Formatting:** Display clearly, perhaps on a new line or with a distinct icon/label.
    -   **Missing Data:** If the data is missing, display an empty string (do not show "N/A" or placeholders).

## Non-Functional Requirements
-   **Performance:** The extraction should not significantly slow down the search process (parsing the existing JSON blob is efficient).
-   **Reliability:** The scraper must gracefully handle changes to the JSON structure (e.g., missing keys).

## Out of Scope
-   Displaying this information in the Terminal Output table (unless explicitly requested later).
-   Searching/Filtering by Agency Name.
