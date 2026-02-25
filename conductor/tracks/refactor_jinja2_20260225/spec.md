# Specification: Refactor to Jinja2 HTML Templating

## Overview
Move away from the 2-step (Markdown -> HTML) rendering process to a streamlined, 1-step HTML generation approach using the **Jinja2** templating engine. This refactoring will eliminate brittle string concatenation in `reporter.py`, improve security via auto-escaping, and drastically simplify dashboard UI development. The CLI tool will focus exclusively on generating the HTML dashboard (`results.html`), dropping the plain-text `results.md` output.

## Functional Requirements

### 1. Dependency Management
- **Add:** Introduce `Jinja2` as a core dependency in `requirements.txt`.
- **Remove:** Completely remove the `markdown` library and its related imports from the codebase.

### 2. Templating Architecture
- Implement a hierarchical template structure using Jinja2 inheritance:
  - `templates/base.html`: The core HTML skeleton, `<head>`, meta tags, and global assets (including the CSS framework).
  - `templates/report.html`: The specific template extending `base.html` to render the property results table and dashboard features.
- Move all HTML string logic currently residing in Python files (`reporter.py`, `dashboard.py`) into these templates.

### 3. CSS Framework & UI Refactoring
- Integrate **Tailwind CSS** (via CDN) into the `base.html` template.
- Refactor the current embedded CSS classes into Tailwind utility classes where applicable.
- Improve the responsive design, ensuring the dashboard table and features work well on mobile/smaller screens.
- Ensure the existing features (Badges, Shortlist, Dismiss, Refresh notes) are preserved visually but implemented cleanly with Tailwind.

### 4. Code Cleanup
- Update `reporter.py` to solely inject the raw `properties` dictionary list into the Jinja environment.
- Remove all `for_html` flags and `markdown` conversion functions from `reporter.py`.
- Update `rightmove_search.py` to remove file I/O operations for `results.md`.

## Non-Functional Requirements
- Maintain the current single-command CLI experience (`python rightmove_search.py <url>`).
- Preserve the speed and efficiency of rendering the final dashboard.

## Out of Scope
- Changing the underlying Rightmove parsing logic or commute calculation logic.
- Adding new dashboard features beyond responsive improvements and styling refactors.