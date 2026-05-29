# Implementation Plan - Amenity Proximity Integration

This plan outlines the steps to integrate OpenStreetMap (Overpass) API to find nearby amenities (supermarkets, gyms, parks, healthcare) for each rental property.

---

## Phase 1: Research and API Client Setup [checkpoint: 0c5d631]
- [x] Task: Research Overpass QL for fetching supermarkets, gyms, parks, and healthcare a1b1a3a
- [x] Task: Implement `AmenityClient` using `requests` or `urllib` to query Overpass (TDD - Red/Green/Refactor) a1b1a3a
- [x] Task: Implement a caching mechanism for API responses to avoid redundant queries (TDD - Red/Green) a1b1a3a
- [x] Task: Conductor - User Manual Verification 'Phase 1: Research and API Client Setup' (Protocol in workflow.md) a1b1a3a

## Phase 2: Core Integration and Calculation [checkpoint: 85aa478]
- [x] Task: Update the property processing loop to call the `AmenityClient` (TDD - Red/Green) fb5aa5f
- [x] Task: Implement logic to calculate distance to the nearest instance of each category (TDD - Red/Green) fb5aa5f
- [x] Task: Add a command-line flag or config setting for the search radius (default 1000m) fb5aa5f
- [x] Task: Conductor - User Manual Verification 'Phase 2: Core Integration and Calculation' (Protocol in workflow.md) 85aa478

## Phase 3: Output and Reporting [checkpoint: 3a93df5]
- [x] Task: Update the Markdown table generator to include the "Nearby Amenities" column (TDD - Red/Green) 0734d0f
- [x] Task: Verify the end-to-end flow with real search results from Rightmove 0734d0f
- [x] Task: Ensure code coverage for new modules is >80% 0734d0f
- [x] Task: Conductor - User Manual Verification 'Phase 3: Output and Reporting' (Protocol in workflow.md) 3a93df5
