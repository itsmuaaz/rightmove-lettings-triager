# Implementation Plan - Property "Vibe" Integration

This plan outlines the steps to integrate LLM-based (e.g., Gemini) "vibe" categorization for each rental property based on its location (postcode/borough).

---

## Phase 1: LLM Client and Prompt Engineering
- [x] Task: Research LLM prompt strategies to categorize London postcodes by safety, reputation, and prestige [e107a87]
- [x] Task: Implement `VibeClient` using the Google Gemini API to query postcode attributes (TDD - Red/Green/Refactor) [e107a87]
- [x] Task: Implement a caching mechanism for postcode lookups to minimize API calls (TDD - Red/Green) [e107a87]
- [x] Task: Conductor - User Manual Verification 'Phase 1: LLM Client and Prompt Engineering' (Protocol in workflow.md) [checkpoint: 5e46622]

## Phase 2: Vibe Scoring and Integration
- [x] Task: Update the property processing loop to call the `VibeClient` for each unique postcode (TDD - Red/Green) [cd3aea0]
- [x] Task: Implement logic to calculate the aggregate "Vibe Score" (1-10) based on LLM attributes (TDD - Red/Green) [cd3aea0]
- [x] Task: Add a short summary tag generator based on the vibe scores (TDD - Red/Green) [cd3aea0]
- [x] Task: Conductor - User Manual Verification 'Phase 2: Vibe Scoring and Integration' (Protocol in workflow.md) [checkpoint: cd3aea0]

## Phase 3: Reporting and Validation
- [x] Task: Update the Markdown table generator to include the "Vibe Score & Summary" column (TDD - Red/Green) [ebaa0a4]
- [x] Task: Verify the end-to-end flow with real search results for disparate London areas (e.g., Richmond vs. Newham) [ebaa0a4]
- [x] Task: Ensure code coverage for new modules is >80% [ebaa0a4]
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Reporting and Validation' (Protocol in workflow.md)
- [ ] Task: Ensure code coverage for new modules is >80%
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Reporting and Validation' (Protocol in workflow.md)
