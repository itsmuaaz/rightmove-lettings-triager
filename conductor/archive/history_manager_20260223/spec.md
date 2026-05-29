# Specification: History Manager & Inbox Style Dashboard

## Overview
Implement a persistent history tracking system to help users distinguish between new, viewed, and dismissed properties. This transforms the dashboard from a static list into a stateful "inbox" of property leads.

## Functional Requirements

### 1. History Persistence
- **Storage:** Maintain a `history.json` file in the project root.
- **Schema:**
  ```json
  {
    "property_id": {
      "first_seen": "ISO8601 Timestamp",
      "last_viewed": "ISO8601 Timestamp (optional)",
      "status": "new | viewed | dismissed"
    }
  }
  ```
- **Logic:**
  - When scraping, if a property ID is NOT in `history.json`, add it with `first_seen = now` and `status = new`.
  - Preserve existing history for known IDs.

### 2. API Endpoint (`dashboard.py`)
- **Endpoint:** `POST /api/history`
- **Payload:** `{"id": "property_id", "action": "view | dismiss | undo_dismiss"}`
- **Behavior:** Updates the `history.json` file based on the action.
  - `view`: Sets `last_viewed` to now, updates status to `viewed` (if not already dismissed).
  - `dismiss`: Updates status to `dismissed`.
  - `undo_dismiss`: Reverts status to `viewed` (or `new` if never viewed).

### 3. User Interface (`results.html` / `reporter.py`)
- **"New" Badge:** Display a prominent "NEW" badge on cards with `status = new`.
- **Viewed State:**
  - Trigger: Clicking "View on Rightmove".
  - Visual: Card opacity reduced (e.g., 0.7).
  - Action: Sends `view` action to API.
- **Dismissal:**
  - Trigger: A new "Hide/Dismiss" button on each card.
  - Visual: Card collapses to a summary row (Address + Price only) and greys out.
  - Action: Sends `dismiss` action to API.
  - Reversal: Clicking the collapsed card expands it and sends `undo_dismiss`.
- **Global Actions:**
  - "Mark All as Seen" button: Marks all currently visible "new" items as "viewed".

## Non-Functional Requirements
- **Performance:** UI must update immediately (optimistic update) without waiting for API response.
- **Compatibility:** Must work within the existing `http.server` implementation (no new framework dependencies).
- **Graceful Degradation:** If the API fails (or server not running), the UI should still allow navigation to Rightmove, simply without saving state.

## Out of Scope
- User accounts (single user system).
- Syncing history across devices.