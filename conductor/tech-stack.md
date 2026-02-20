# Tech Stack: UK Letting Researcher

## Languages
- **Python 3.x:** Primary scripting language for parsing logic and data manipulation.

## Core Libraries (Python Standard Library)
- **`json`:** Used for parsing the JSON data found within Rightmove's HTML structure.
- **`re`:** For regular expression matching to extract the embedded script tags.
- **`math`:** To perform geographical distance calculations (Haversine formula).
- **`subprocess`:** To execute external commands like `curl`.
- **`urllib`:** For URL parsing, encoding, and constructing search query parameters.
- **`os`:** For interacting with environment variables.
- **`venv`:** For managing project dependencies in a virtual environment.

## External Tools
- **`curl`:** Used as the primary data fetching mechanism, configured with a browser-like User-Agent to bypass simple anti-bot measures.
- **TfL Unified API:** Primary data source for calculating public transport commute times in London.
- **OpenStreetMap (Overpass) API:** Used for finding nearby amenities (supermarkets, gyms, parks, etc.).
- **`pytest` / `pytest-cov`:** For automated testing and code coverage verification.
- **`markdown`:** Python library for converting Markdown text to HTML.

## Output Format
- **Rich Markdown & HTML:** Search results are formatted as an enriched Markdown table (`results.md`) and a styled HTML dashboard (`results.html`) for browser viewing.
