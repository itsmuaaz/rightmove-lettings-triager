# Implementation Plan - TfL/Google Maps API Integration

This plan outlines the steps to replace straight-line distance calculations with real-world commute times using the TfL or Google Maps API.

## User Review Required

> [!IMPORTANT]
> To proceed with Phase 2, you will need to provide either a TfL API Key (App ID/Key) or a Google Maps API Key. Please ensure these are available as environment variables: `TFL_APP_ID`, `TFL_APP_KEY`, or `GOOGLE_MAPS_API_KEY`.

---

## Phase 1: Research and Setup [checkpoint: 917cb50]
- [x] Task: Research TfL and Google Maps Distance Matrix API limits and requirements 05028f9
- [x] Task: Implement environment variable loading for API keys 7498f0a
- [x] Task: Conductor - User Manual Verification 'Phase 1: Research and Setup' (Protocol in workflow.md)

## Phase 2: API Client and Core Logic
- [x] Task: Write failing tests for the API client (TDD - Red Phase) 994eae6
- [x] Task: Implement a basic API client to fetch journey times (TDD - Green Phase) 994eae6
- [x] Task: Refactor API client for error handling and fallbacks (TDD - Refactor) 397aa1f
- [ ] Task: Write failing tests for the commute calculation logic (TDD - Red Phase)
- [ ] Task: Integrate API client into the main calculation loop (TDD - Green Phase)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: API Client and Core Logic' (Protocol in workflow.md)

## Phase 3: Reporting and Validation
- [ ] Task: Update the Markdown table generator to include "Commute Time"
- [ ] Task: Verify end-to-end flow with real search results
- [ ] Task: Ensure code coverage for new modules is >80%
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Reporting and Validation' (Protocol in workflow.md)
