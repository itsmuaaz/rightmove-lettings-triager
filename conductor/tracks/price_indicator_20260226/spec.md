# Specification: Relative Price Indicator

## Overview
This feature adds a visual, color-coded circular marker next to the property price in the dashboard table. The color indicates how cheap or expensive the property is relative to the current search results, mapping from Green (cheapest) to Red (most expensive) via an HSL color gradient.

## Functional Requirements
- **Numerical Extraction:** The system must reliably parse raw price strings (e.g., "£2,000 pcm") into numerical values.
- **Global Boundaries:** The system must identify the minimum and maximum property prices within the current result set.
- **Color Calculation:** Each property must receive a calculated HSL color value where `hsl(120, ...)` represents the minimum price (Green) and `hsl(0, ...)` represents the maximum price (Red). Intermediate prices must fall on this gradient.
- **UI Integration:** The color indicator must be rendered as a small circular marker adjacent to the price in the `report.html` template.

## Edge Cases
- Properties with missing, non-numeric, or "POA" prices should not display an indicator or should display a neutral (gray) indicator.
- If all properties have the exact same price (min == max), the indicator should default to a neutral mid-point color (e.g., Yellow).

## Out of Scope
- Client-side dynamic recalculation as new properties are fetched (the server-side Jinja render will dictate the colors for that specific report generation).
- Adjusting the color scale based on external market data or averages; the scale is strictly relative to the *current search results*.