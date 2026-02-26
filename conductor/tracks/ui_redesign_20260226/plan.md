# Implementation Plan - UI/UX Redesign

## Phase 1: Design System Foundation
- [ ] Task: Update `base.html` to inject the new Tailwind configuration (colors, fonts, etc.)
- [ ] Task: Update `report.html` body and main container to use the new `bg-page` and `text-text-primary` classes
- [ ] Task: Verify that the basic layout renders correctly with the new font (Inter) and background color
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Design System Foundation' (Protocol in workflow.md)

## Phase 2: Core Components Refactor
- [ ] Task: Refactor the "Shortlist" section in `report.html` to use the new Card design (Grid View)
    - [ ] Update container styles (`bg-surface`, `rounded-lg`, `shadow-sm`)
    - [ ] Update image styles (`w-full`, `h-48`, `object-cover`)
    - [ ] Update action button styles (muted text, uppercase)
- [ ] Task: Refactor the "Main Results Table" in `report.html` to use the new Row design
    - [ ] Implement `property-row` semantic classes for states (Shortlisted, New, Dismissed)
    - [ ] Add the custom CSS for row borders in `base.html` or `<style>` block
    - [ ] Update cell padding and text alignment
- [ ] Task: Refactor Links (TfL, Google Maps) to use the new "Pill" design (`rounded-full`, `bg-slate-100`, `text-brand-primary`)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Components Refactor' (Protocol in workflow.md)

## Phase 3: Data Visualization & Logic Support
- [ ] Task: Update `reporter.py` (or helper) to generate the new CSS classes for Score bubbles (Green > 80, Amber 50-79, Red < 50)
    - [ ] TDD: Write unit tests for the color logic
    - [ ] Implement logic
- [ ] Task: Update `report.html` to display Score bubbles using the new logic/classes
- [ ] Task: Refactor Price display in `report.html` (bold primary text for PCM, secondary for PW, remove floating dots if needed)
- [ ] Task: Refactor Amenities list in `report.html` (`leading-relaxed`, `text-text-secondary`, `opacity-75` icons)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Data Visualization & Logic Support' (Protocol in workflow.md)

## Phase 4: Responsiveness & Final Polish
- [ ] Task: Optimize the "Shortlist" Grid for mobile (collapse to 1 column: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`)
- [ ] Task: Optimize the "Main Results Table" for mobile (ensure horizontal scrolling or stacked layout if feasible)
- [ ] Task: Verify all text contrast meets accessibility standards
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Responsiveness & Final Polish' (Protocol in workflow.md)
