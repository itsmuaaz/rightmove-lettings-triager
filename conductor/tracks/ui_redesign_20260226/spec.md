# Specification: UI/UX Redesign - Modern Light Theme

## 1. Overview
This track focuses on a comprehensive visual redesign of the Letting Search Platform to improve accessibility, visual hierarchy, and overall user experience. The redesign will implement a modern, clean aesthetic using a light-themed color palette, semantic design tokens, and improved component styling (Pills, Cards, Tables).

**Scope:**
- **Fully Responsive:** The new design must work seamlessly on mobile, tablet, and desktop.
- **Light Mode Only:** Strictly adhere to the specified neutral/light palette.
- **Logic Support:** Minor Python logic adjustments are permitted to support dynamic styling (e.g., score color calculation).

## 2. Functional Requirements

### 2.1 Design Tokens (Tailwind Configuration)
- **Objective:** Establish a consistent design system via Tailwind configuration in `base.html`.
- **Requirements:**
    - Extend the Tailwind theme with the specified `colors` and `fontFamily`.
    - **Neutral Palette:** `page`, `surface`, `border-subtle`, `border-highlight`, `border-new`.
    - **Text Colors:** `text-primary`, `text-secondary`, `text-tertiary`.
    - **Semantic Colors:** `brand-primary`, `state-highlight`, `state-new`, `state-good`, `state-bad`, `state-avg`.
    - **Font:** 'Inter' stack as the default sans-serif font.

### 2.2 Typography & Text Contrast
- **Objective:** Improve legibility and accessibility.
- **Requirements:**
    - Update `<body>` to use `bg-page`, `text-text-primary`, and `font-sans`.
    - Property Titles: Use `text-lg`, `font-semibold`, `text-brand-primary` (no underline unless hovered).
    - Secondary Text (Amenities, Vibes): Use `text-text-secondary` and `font-weight: 400`.
    - Timestamps: Use `text-text-tertiary`.

### 2.3 Component: Table Rows (List View)
- **Objective:** Reduce visual clutter and improve state indication.
- **Requirements:**
    - **Default:** White background (`bg-surface`), subtle bottom border.
    - **Shortlisted:** Pale cream background (`bg-state-highlight`) with a thick amber left border (`border-l-4 border-highlight`).
    - **New:** Pale blue background (`bg-state-new`) with a thick light blue left border (`border-l-4 border-new`).
    - **Dismissed:** Reduced opacity (`opacity-60`), grayscale filter, light grey background.
    - **Interaction:** Smooth transition on hover (`hover:bg-gray-50` for default rows).

### 2.4 Component: Pills (Links & Badges)
- **Objective:** Modernize links and status indicators.
- **Requirements:**
    - **Links (TfL, Google Maps):** Style as "pills" - `rounded-full`, `bg-slate-100`, `text-brand-primary`, `text-xs`, `font-medium`, `hover:bg-slate-200`.
    - **Status Badges (New, Shortlisted):** Use consistent pill styling with appropriate semantic colors.

### 2.5 Component: Cards (Grid View - Shortlist)
- **Objective:** Create a cohesive, card-based layout for the shortlist.
- **Requirements:**
    - **Container:** `bg-surface`, `rounded-lg`, subtle shadow (`shadow-sm`), border (`border-border-subtle`).
    - **Image:** Full width (`w-full`), fixed height (`h-48`), `object-cover`.
    - **Actions:** "Remove" button styled as muted text (`text-text-tertiary`, `uppercase`, `text-xs`, `font-medium`) that turns red on hover.

### 2.6 Data Formatting
- **Objective:** Enhance the visualization of key metrics.
- **Requirements:**
    - **Score Bubbles:** Perfect circle (`w-8 h-8`), centered text, white text. Background color determined dynamically (Green > 80, Amber 50-79, Red < 50).
    - **Price:** Bold primary text for PCM, secondary text for PW. Remove floating dots if they clutter the view; prefer text color or subtle background indicators if needed.
    - **Amenities:** Clean list with `leading-relaxed`, muted icons (`opacity-75`).

## 3. Non-Functional Requirements
- **Performance:** CSS changes should not degrade rendering performance.
- **Accessibility:** Text contrast must meet WCAG AA standards (implied by the new palette).
- **Responsiveness:** The "List View" (Table) must remain usable on mobile (e.g., horizontal scroll or stacked layout). The "Grid View" should collapse to 1 column on mobile.

## 4. Out of Scope
- Dark Mode implementation.
- Major structural changes to the Python backend (beyond style helpers).
- Adding new data sources or metrics.

## 5. Acceptance Criteria
- [ ] `base.html` contains the correct Tailwind configuration.
- [ ] All text is legible and uses the new color palette.
- [ ] Shortlisted items are clearly visually distinct (Cream bg + Amber border).
- [ ] "New" items are clearly visually distinct (Blue bg + Blue border).
- [ ] Links look like clickable "pills".
- [ ] The Shortlist section uses the new Card design.
- [ ] Scores are displayed in colored circular badges.
- [ ] The design is fully responsive and looks good on a mobile device simulator.
