# Specification: Richer Output Format (Enriched MD & Styled HTML)

## Overview
Implement a robust reporting system that replaces simple terminal output with an enriched Markdown file (`results.md`) and a styled HTML file (`results.html`). This system will leverage embedded CSS to provide visual cues and include property images for better evaluation.

## Functional Requirements
- **Enriched Markdown Output**:
    - Generate `results.md` containing a rich table.
    - Columns: Image, Price, Commute, Distance, Details (Bedrooms + Type), Address, Added On, Link.
    - Thumbnails: Display property images with a fixed width of 150px.
    - Color Coding: Inject inline HTML spans with semantic classes (e.g., `<span class="badge-green">`) into Markdown cells for styling.
- **Styled HTML Output**:
    - Convert `results.md` into `results.html` using the `python-markdown` library.
    - Use a master HTML template with embedded CSS to style the Markdown-generated HTML.
    - CSS "Traffic Light" System:
        - **Commute Time**: Green (<20m), Amber (20-40m), Red (>40m).
        - **Price/Recency**: Visual highlights for competitive prices or new listings.
- **Enhanced Data Extraction**:
    - Extract `propertyImages`, `bedrooms`, and `firstPublishedDate` from Rightmove's JSON blob.
- **CLI Logging**:
    - Maintain clean `stdout` with simple progress logs.
    - Output final file paths: "Report saved to results.md and results.html".

## Technical Requirements
- **Library**: Use `python-markdown` with the `tables` extension for conversion.
- **CSS**: Embed all styling within the `results.html` file to ensure it works offline and without external dependencies.
- **Encoding**: Ensure proper handling of the "£" symbol and special characters.

## Acceptance Criteria
1. The script successfully generates both `results.md` and `results.html`.
2. Property images are displayed at 150px width in both files.
3. Commute times are correctly color-coded based on the defined thresholds.
4. All new data points (bedrooms, added date) are visible in the output.
5. The HTML file renders correctly in standard browsers (Chrome, Safari, Firefox).

## Out of Scope
- Interactive JavaScript-based sorting or filtering (e.g., DataTables).
- Map visualizations.
- Supporting external CSS files.
