# Specification: Smart Scoring System

## Overview
This track introduces a "Smart Score" (0-100) for each property to transform the application from a list of data points into a ranked decision matrix. The score is a weighted aggregate of Price, Commute Time, Vibe, and Freshness, designed to help users quickly identify the best trade-offs.

## Functional Requirements

### 1. Scoring Engine
- **Algorithm:** Implement a weighted sum formula:
  $$ Score = (W_P 	imes S_{price}) + (W_C 	imes S_{commute}) + (W_V 	imes S_{vibe}) + (W_F 	imes S_{fresh}) $$
- **Weights:**
  - **Commute ($W_C$):** 40%
  - **Price ($W_P$):** 30%
  - **Vibe ($W_V$):** 20%
  - **Freshness ($W_F$):** 10%
- **Normalization:**
  - **Price:** Relative to the *current search results* Min/Max. Cheapest = 100, Most Expensive = 0.
  - **Commute:** Linear decay from 0 to 60 minutes. $\le$ 20 mins = 100, $\ge$ 60 mins = 0.
  - **Vibe:** Scale the existing 1-10 score to 0-100.
  - **Freshness:** Linear decay over 7 days. < 24 hours = 100, > 7 days = 0.
- **Missing Data Handling:**
  - If a component (e.g., Commute or Vibe) is missing (`None`), its weight is **redistributed proportionally** to the remaining valid components.
  - If critical data (Price) is missing, the score is 0.

### 2. Backend Integration
- **Global Context:** The scoring logic must run *after* all properties are fetched to determine global Min/Max values for Price.
- **Data Model:** Update the property dictionary to include:
  - `smart_score` (float, 0-100)
  - `score_breakdown` (dict, for debugging/tooltips)

### 3. Dashboard Visualization
- **Badge:** Display a color-coded numeric badge on each property card:
  - 🟢 **90+** (Excellent)
  - 🟡 **70-89** (Good)
  - ⚪ **<70** (Average/Poor)
- **Sorting:** Set "Smart Score (High to Low)" as the default sort order for the results.
- **Tooltip:** Hovering over the badge reveals the score breakdown (e.g., "Price: 25/30, Commute: 35/40...").

### 4. Configuration
- **External Config:** Move all weights and thresholds (Max Commute = 60m, Freshness Decay = 7d) to `config.py` to allow easy tuning.

## Non-Functional Requirements
- **Performance:** The scoring calculation must be instant (< 100ms for 500 properties) and not block the UI rendering.
- **Reliability:** The system must gracefully handle edge cases like "Added on: Yesterday" or "Reduced today" for freshness calculations.

## Out of Scope
- User-adjustable weights via the UI (CLI/Config only for now).
- Machine learning or user-feedback loops to adjust weights.