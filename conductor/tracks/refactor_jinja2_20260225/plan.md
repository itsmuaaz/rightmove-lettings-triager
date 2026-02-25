# Implementation Plan - Refactor to Jinja2

## Phase 1: Setup and Dependency Management [checkpoint: 30d75ff]
- [x] Task: Update `requirements.txt` to remove `markdown` and add `Jinja2`
- [x] Task: Create `templates/base.html` with Tailwind CSS CDN integration
- [x] Task: Create `templates/report.html` extending `base.html`
- [x] Task: Conductor - User Manual Verification 'Phase 1: Setup and Dependency Management' (Protocol in workflow.md)

## Phase 2: Refactor Reporter Class [checkpoint: 58a7310]
- [x] Task: Update `tests/test_reporter.py` to test Jinja2 rendering instead of markdown string generation (TDD - Red Phase)
- [x] Task: Update `reporter.py` to use `jinja2.Environment` and remove all string-based HTML injection logic (TDD - Green/Refactor)
- [x] Task: Implement the HTML layout in `templates/report.html` using Tailwind CSS, moving rendering logic out of Python
- [x] Task: Conductor - User Manual Verification 'Phase 2: Refactor Reporter Class' (Protocol in workflow.md)

## Phase 3: Integration & Cleanup
- [x] Task: Update `tests/test_dashboard_integration.py` and `tests/test_rightmove_search.py` reflecting the new 1-step architecture
- [x] Task: Update `dashboard.py` to serve the new Jinja2 rendered HTML and simplify page refresh logic
- [x] Task: Update `rightmove_search.py` to stop writing `results.md` and only handle the `results.html` report
- [x] Task: Delete the old `reporter_template.html` and any dead CSS/Markdown helper functions
- [x] Task: Conductor - User Manual Verification 'Phase 3: Integration & Cleanup' (Protocol in workflow.md)