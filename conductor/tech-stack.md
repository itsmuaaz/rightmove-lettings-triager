# Tech Stack: UK Letting Researcher

## Languages
- **Python 3.x:** Primary scripting language for parsing logic and data manipulation.

## Core Libraries (Python Standard Library)
- **`json`:** Used for parsing the JSON data found within Rightmove's HTML structure.
- **`threading`:** For running the dashboard server concurrently with the data processing loop.
- **`re`:** For regular expression matching to extract the embedded script tags.
- **`math`:** To perform geographical distance calculations (Haversine formula).
- **`subprocess`:** To execute external commands like `curl`.
- **`urllib`:** For URL parsing, encoding, and constructing search query parameters.
- **`os`:** For interacting with environment variables.
- **`venv`:** For managing project dependencies in a virtual environment.
- **`http.server`:** For serving the local interactive dashboard.

## External Tools
- **`curl`:** Used as the primary data fetching mechanism, configured with a browser-like User-Agent to bypass simple anti-bot measures.
- **TfL Unified API:** Primary data source for calculating public transport commute times in London. Commute times are standardized to a "Tuesday 9:00 AM" benchmark and cached with metadata to support manual data refreshes.
- **OpenStreetMap (Overpass) API:** Used for finding nearby amenities (supermarkets, gyms, parks, etc.).
- **`pytest` / `pytest-cov`:** For automated testing and code coverage verification.
- **`jinja2`:** Templating engine for generating the HTML report.

## Output Format
- **Rich HTML:** Search results are formatted as a styled HTML dashboard (`results.html`) using **Jinja2** templates and **Tailwind CSS**.
