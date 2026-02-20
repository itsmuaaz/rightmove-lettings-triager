# Initial Concept

# Product Guide: Rightmove Property Search and Commute Calculator

## Vision
A tool that automates searching for properties on Rightmove and calculates the distance from a user's work location to help in finding a home with a manageable commute.

## Target Users
People who are looking for rental properties in London and want to quickly compare options based on price and distance to their workplace.

## Core Features
- **Search Automation:** Fetches search results directly from a Rightmove URL.
- **Auto-Pagination:** Automatically browses through all available result pages.
- **Distance Calculation:** Calculates the straight-line distance (miles) from each property to a specified work location (e.g., N1C 4AG).
- **Consolidated Output:** Combines all properties into a single, sorted Markdown table for easy comparison.

## Architecture
A standalone Python script that uses `curl` for fetching data and standard libraries for processing. It relies on the Next.js JSON blob found within Rightmove's HTML source for its data extraction.

## Future Goals
- Integrate public transport commute times using TfL/Google APIs.
- Highlight "new" properties since the last search.
- Add support for multiple destinations and custom user agents.
