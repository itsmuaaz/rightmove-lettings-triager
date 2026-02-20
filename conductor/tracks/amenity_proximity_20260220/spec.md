# Specification: Amenity Proximity Feature

## Overview
This feature adds the ability to search for and display nearby amenities for each rental property. It helps users evaluate the "suitability" of a location based on its proximity to essential services and leisure facilities.

## Functional Requirements
- **Amenity Categories**: Support searching for Supermarkets, Gyms/Fitness centers, Parks/Green Spaces, and Healthcare facilities.
- **Data Source**: Use the OpenStreetMap (Overpass) API for fetching geographical data.
- **Search Radius**:
    - Default radius: 1km.
    - Configuration: Must be user-configurable (e.g., via a CLI flag or config file).
- **Distance Calculation**: Calculate the straight-line distance from the property coordinates to each amenity.
- **Output Enhancement**:
    - Add a new "Nearby Amenities" column to the generated Markdown table.
    - Display the nearest instance of each category with its distance (e.g., "Sainsbury's (400m), PureGym (600m)").

## Non-Functional Requirements
- **Performance**: Minimize API overhead by using efficient Overpass queries (e.g., querying multiple categories in one call).
- **Reliability**: Implement error handling for API timeouts or unavailable data.
- **No Dependencies**: Maintain the project's preference for Python standard libraries where possible, though a library like `requests` may be needed for API interaction.

## Acceptance Criteria
1. The script accepts a radius parameter (e.g., `--radius 1500`).
2. The final Markdown report contains a "Nearby Amenities" column.
3. Distances for found amenities are accurately calculated and displayed in meters.
4. If no amenities are found within the radius for a category, it is gracefully omitted or marked as "None nearby".

## Out of Scope
- Commute time calculations for amenities (walking time/routing).
- Quality ratings or reviews for amenities.
- Support for other mapping APIs (Google/Mapbox) for this specific feature.
