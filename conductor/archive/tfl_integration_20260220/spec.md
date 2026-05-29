# Specification: TfL/Google Maps API Integration

## Overview
Replace the current straight-line (Haversine) distance calculation with real commute times using a public transport API.

## Requirements
- Support fetching travel times from property coordinates to the work location (N1C 4AG).
- Prefer TfL API for London-based properties, or Google Maps Distance Matrix API as a fallback.
- Handle API authentication securely (e.g., via environment variables).
- Update the Markdown output table to include a "Commute Time" column.
- Fallback to straight-line distance if the API call fails or the property is outside the API's coverage.

## Success Criteria
- The Markdown table displays accurate commute times (e.g., "35 mins").
- No API keys are committed to version control.
- The script handles rate limiting and connectivity issues gracefully.
