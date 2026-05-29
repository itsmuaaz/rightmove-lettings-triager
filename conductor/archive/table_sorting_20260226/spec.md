# Specification: Table Sorting & Commute Optimization

## Overview
Implement interactive column sorting for the property dashboard table. Users can sort properties by Price, Smart Score, Vibe, Commute Time, and Added Date. The Commute column will feature a specialized mechanism to toggle between sorting by "Public Transport", "Cycling", or the "Minimum" of both. The selected sort state will be persisted in the URL query parameters, ensuring the view remains consistent on refresh.

## Functional Requirements

### 1. Column Headers & Interaction
*   **Clickable Headers:** The following table headers must be clickable to trigger a sort:
    *   Price
    *   Smart Score
    *   Vibe (Safety/Score)
    *   Commute
    *   Added On
*   **Toggle Logic:** Clicking a header toggles between **Ascending** and **Descending** order.
*   **Visual Feedback:** The active sort column must display an arrow icon (&#x25B2;/&#x25BC;) indicating the current sort direction. Inactive columns should have no arrow.

### 2. Commute Column Specifics
*   **Sort Modes:** The Commute column supports three distinct sort modes:
    *   `min`: Minimum of (Public Transport, Cycling) [Default]
    *   `transport`: Public Transport time only.
    *   `cycling`: Cycling time only.
*   **Selection Mechanism:** The Commute header must include a UI element (e.g., a small dropdown or sub-menu) to select the active sort mode.
    *   Selecting a mode updates the table sort order immediately.
    *   The header label or icon should reflect the currently selected mode (e.g., "Commute (Cycling)").

### 3. Sorting Logic
*   **Price:** Numeric sort based on the parsed monthly price (Low &harr; High).
*   **Smart Score:** Numeric sort based on the calculated Smart Score (High &harr; Low).
*   **Vibe:** Numeric sort based on Vibe Score (if available) or alphabetical by category.
*   **Added On:** Date sort based on the listing date (Newest &harr; Oldest).
*   **Commute:** Numeric sort based on the selected mode (`min`, `transport`, `cycling`).

### 4. Persistence
*   **URL Parameters:** The application must use URL query parameters to store the sort state.
    *   `sort`: The field to sort by (e.g., `price`, `score`, `commute`).
    *   `order`: The direction (`asc` or `desc`).
    *   `mode`: The commute mode (`min`, `transport`, `cycling`) - *Only relevant when sort=commute*.
*   **State Restoration:** On page load, the application must read these parameters and apply the correct sort order before rendering.

### 5. Default State
*   If no parameters are present, the default sort shall be: **Smart Score (Descending)**.

## Non-Functional Requirements
*   **Performance:** Sorting should be efficient enough to not noticeably delay page load for <500 properties.
*   **Compatibility:** Ensure the sorting logic handles `None` or missing values gracefully (e.g., properties with unknown price or commute should appear at the end).

## Acceptance Criteria
*   [ ] Clicking "Price" sorts the list by price; clicking again reverses it.
*   [ ] Clicking "Smart Score" sorts the list by score; clicking again reverses it.
*   [ ] The "Commute" header has a dropdown/menu to select "Transport", "Cycling", or "Min".
*   [ ] Selecting "Cycling" re-sorts the list based on cycling time.
*   [ ] Reloading the page with `?sort=price&order=desc` preserves the sort.
*   [ ] The UI displays a clear arrow indicator on the active column.
