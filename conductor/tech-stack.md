# Tech Stack: Rightmove Property Search and Commute Calculator

## Languages
- **Python 3.x:** Primary scripting language for parsing logic and data manipulation.

## Core Libraries (Python Standard Library)
- **`json`:** Used for parsing the JSON data found within Rightmove's HTML structure.
- **`re`:** For regular expression matching to extract the embedded script tags.
- **`math`:** To perform geographical distance calculations (Haversine formula).
- **`subprocess`:** To execute external commands like `curl`.
- **`urllib`:** For URL parsing, encoding, and constructing search query parameters.

## External Tools
- **`curl`:** Used as the primary data fetching mechanism, configured with a browser-like User-Agent to bypass simple anti-bot measures.

## Output Format
- **Markdown:** All search results are formatted as Markdown tables for easy readability and integration into other documents or tools.
