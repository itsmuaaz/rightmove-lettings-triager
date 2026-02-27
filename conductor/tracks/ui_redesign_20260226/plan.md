# Implementation Plan - UI/UX Redesign

## Phase 1: Design System Foundation [checkpoint: 7adfaa4]
- [x] Task: Update `base.html` to inject the new Tailwind configuration (colors, fonts, etc.)
- [x] Task: Update `report.html` body and main container to use the new `bg-page` and `text-text-primary` classes
- [x] Task: Verify that the basic layout renders correctly with the new font (Inter) and background color
- [x] Task: Conductor - User Manual Verification 'Phase 1: Design System Foundation' (Protocol in workflow.md)

## Phase 2: Core Components Refactor [checkpoint: 7441cee]
- [x] Task: Refactor the "Shortlist" section in `report.html` to use the new Card design (Grid View)
    - [x] Update container styles (`bg-surface`, `rounded-lg`, `shadow-sm`)
    - [x] Update image styles (`w-full`, `h-48`, `object-cover`)
    - [x] Update action button styles (muted text, uppercase)
- [x] Task: Refactor the "Main Results Table" in `report.html` to use the new Row design
    - [x] Implement `property-row` semantic classes for states (Shortlisted, New, Dismissed)
    - [x] Add the custom CSS for row borders in `base.html` or `<style>` block
    - [x] Update cell padding and text alignment
- [x] Task: Refactor Links (TfL, Google Maps) to use the new "Pill" design (`rounded-full`, `bg-slate-100`, `text-brand-primary`)
- [x] Task: Implement collapsible toggle for Shortlisted Properties section
- [x] Task: Conductor - User Manual Verification 'Phase 2: Core Components Refactor' (Protocol in workflow.md)

## Phase 3: Data Visualization & Logic Support [checkpoint: 329f7da]
- [x] Task: Update `reporter.py` (or helper) to generate the new CSS classes for Score bubbles (Green > 80, Amber 50-79, Red < 50)
    - [x] TDD: Write unit tests for the color logic
    - [x] Implement logic
- [x] Task: Update `report.html` to display Score bubbles using the new logic/classes
- [x] Task: Refactor Price display in `report.html` (bold primary text for PCM, secondary for PW, remove floating dots if needed)
- [x] Task: Refactor Amenities list in `report.html` (`leading-relaxed`, `text-text-secondary`, `opacity-75` icons)
- [x] Task: Conductor - User Manual Verification 'Phase 3: Data Visualization & Logic Support' (Protocol in workflow.md)

## Phase 4: Responsiveness & Final Polish [checkpoint: bed1990]
- [x] Task: Optimize the "Shortlist" Grid for mobile (collapse to 1 column: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`)
- [x] Task: Optimize the "Main Results Table" for mobile (ensure horizontal scrolling or stacked layout if feasible)
- [x] Task: Verify all text contrast meets accessibility standards
- [x] Task: Implement user feedback: Increase text size, reduce padding, modernize icons, verify border colors
## Phase 4.2: Final User Refinements
- [x] Task: Fix vertical alignment of Actions cell (remove align-top)
- [x] Task: Fix left border color for starred properties (debug CSS specificity)
- [x] Task: Move TfL/Google Maps links to the Commute cell
## Phase 4.3: Final Fixes (Border & Pills) [checkpoint: 7f46501]
- [x] Task: Force orange border for starred properties (use !important or target first child)
- [x] Task: Revert Pill size to text-xs/px-3 and full text "Google Maps" (and further refinements: vertical stack, text-sm)
## Phase 4.4: Final Polish (Tooltips & Spacing) [checkpoint: c31b3ae]
- [x] Task: Fix Smart Score tooltip trigger scope (move 'group' class)
- [x] Task: Compact Pill layout (reduce padding/spacing, ensure inline width)
- [x] Task: Conductor - User Manual Verification 'Phase 4.4: Final Polish' (Protocol in workflow.md)
