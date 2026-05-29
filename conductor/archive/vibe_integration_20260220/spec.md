# Specification: Property "Vibe" and Safety Integration

## Overview
This feature enhances the search results by capturing the "vibe," safety, reputation, and prestige of each property's location. It helps users distinguish between properties that might look similar on paper (price, commute, amenities) but are situated in vastly different environments (e.g., Richmond vs. Newham).

## Functional Requirements
- **Vibe Categorization**: Use an LLM (e.g., Gemini) to categorize properties based on their postcode/borough.
- **Metrics**: Each property will be evaluated across four key dimensions:
    - **Safety/Crime Rate**: General perception and statistical safety of the area.
    - **Reputation/Prestige**: The historical prestige or "status" of the neighborhood.
    - **Interest/Vibe**: Density of nightlife, cafes, and cultural activities.
    - **Tranquility/Peace**: Proximity to green spaces and overall noise/bustle levels.
- **Scoring**: A combined "Vibe Score" (e.g., 1-10) will be calculated based on these dimensions.
- **Output Enhancement**:
    - Add a "Vibe Score & Summary" column to the generated Markdown table.
    - Provide a short summary tag (e.g., "7/10 - Prestigious & Quiet").

## Non-Functional Requirements
- **Efficiency**: Batch postcode-to-vibe lookups to minimize LLM API calls and costs.
- **Consistency**: Ensure the LLM uses a consistent scoring rubric for common London areas.
- **No External Data Dependencies**: Rely on LLM internal knowledge rather than scraping third-party safety/reputation sites for this initial version.

## Acceptance Criteria
1. The final report contains a "Vibe Score & Summary" column.
2. The Vibe Score is accurately reflected in the summary (e.g., a score of 9 is described as "Excellent").
3. Properties in notoriously "rough" or "uninteresting" areas receive lower scores than those in "prestigious" or "safe" areas, as per the user's example.
4. If the postcode lookup fails, a fallback "Unknown" is displayed.

## Out of Scope
- Real-time crime statistics from Government APIs.
- User-customizable weights for the Vibe Score (e.g., "safety is more important than prestige").
- Visual maps or heatmaps for vibes.
