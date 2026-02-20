# Initial Concept

# Product Guide: UK Letting Researcher

## Vision
A tool that automates searching for properties on Rightmove and calculates the distance from a user's work location to help in finding a home with a manageable commute.

## Target Users
People who are looking for rental properties in London and want to quickly compare options based on price and distance to their workplace.

## Core Features
- **Search Automation:** Fetches search results directly from a Rightmove URL.
- **Auto-Pagination:** Automatically browses through all available result pages.
- **Commute calculation:** Calculates real-world commute times (Public Transport & Cycling) using the TfL API, with straight-line distance as a fallback.
- **Amenity Proximity:** Identifies nearby supermarkets, gyms, parks, and healthcare facilities using OpenStreetMap data.
- **Rich Reporting:** Generates a consolidated Markdown report and a styled HTML dashboard with property images, color-coded metrics, and direct navigation links (Google Maps, TfL).

## Architecture
A standalone Python script that uses `curl` for fetching data and standard libraries for processing. It relies on the Next.js JSON blob found within Rightmove's HTML source for its data extraction.

## Future Goals
- Highlight "new" properties since the last search.
- Add support for multiple destinations and custom user agents.
