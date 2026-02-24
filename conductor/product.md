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
- **Commute Stability:** Standardizes commute calculations to a consistent benchmark (Next Tuesday at 9:00 AM) to ensure fair comparison across properties, with an option to manually force-refresh data.
- **Amenity Proximity:** Identifies nearby supermarkets, gyms, parks, and healthcare facilities using OpenStreetMap data.
- **Rich Reporting:** Generates a consolidated Markdown report and a styled HTML dashboard with property images, color-coded metrics, and direct navigation links (Google Maps, TfL).
- **Interactive Dashboard:** Serves a local web interface where users can add persistent notes, shortlist favorites, and dismiss unwanted properties.
- **History Manager:** Tracks 'New', 'Viewed', 'Shortlisted', and 'Dismissed' property states across search sessions to prevent redundant analysis.
- **Triage Workflow:** Features a high-visibility 'Shortlist' state and a top-level summary section for quick navigation to favorite properties.
- **TfL Client Optimization:** Implements robust caching and rate limiting to ensure reliable and efficient commute time calculations, preventing API throttling.

## Architecture
A standalone Python script that uses `curl` for fetching data and standard libraries for processing. It relies on the Next.js JSON blob found within Rightmove's HTML source for its data extraction.

## Future Goals
- Highlight "new" properties since the last search.
- Add support for multiple destinations and custom user agents.
