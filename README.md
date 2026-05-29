# Rightmove Lettings Triager 🏡🚇📊

**The Problem:** Searching for London rentals on Rightmove is painfully tedious. You have to copy addresses, manually plug them into Google Maps or Citymapper to calculate commute times, research if neighborhoods are safe/lively, check if supermarkets or parks are nearby, and somehow keep track of flats you’ve already dismissed, viewed, or shortlisted.

**The Goal:** This script automates that entire research and evaluation loop. It scrapes properties directly from Rightmove, enriches them with multi-modal commute times (TfL), local amenities (OpenStreetMap), and neighborhood vibes (Gemini AI), and aggregates them into a stateful, interactive dashboard where you can easily evaluate, shortlist, and add notes to properties.

---

> 💡 **HOT TIP (Advanced Flat-Hunting Workflow):** Set up a saved search with **Email Alerts** on Rightmove for your desired area. Whenever you receive a new alert email, simply copy the URL from the email, feed it into this script, and open your dashboard. The program's built-in **History Manager** will automatically filter out any flats you've already dismissed or viewed, highlighting only the **brand-new listings** with their fully enriched metrics instantly!

---

![Rightmove Lettings Triager Dashboard](./screenshot.png)

---

## 🛠️ Prerequisites
Before running the script, ensure you have:
*   **Python 3.11+** (The project uses the standard `tomllib` library, which requires Python 3.11 or newer).
*   **Active Internet Connection** (To fetch live listings from Rightmove, commute data from TfL, and local amenities from OpenStreetMap).
*   **Google Gemini CLI / API Key** (To query vibes and neighborhood insights).

*Note on TfL Commute calculations:* **No TfL API credentials are required!** The script works perfectly out of the box anonymously. If you want higher rate limits and faster querying, you can register for free credentials at the [TfL Developer Portal](https://api-portal.tfl.gov.uk/) and add them to your setup, but it is completely optional.

---

## 🌟 Core Features

*   **Automated Scraping & Auto-Pagination:** Provide page 1 of any Rightmove search URL, and the script automatically browses through all result pages to extract every flat.
*   **History & Triage Manager:** Tracks the state of flats (`New`, `Viewed`, `Shortlisted`, `Dismissed`) across sessions in `history.json` to prevent redundant analysis.
*   **Multi-Modal Commute (TfL API):** Calculates exact Public Transport and Cycling travel times to your office, standardized to a *Tuesday 9:00 AM benchmark* for fair comparison. Includes Peak/Off-Peak fare costs.
*   **Amenity Proximity (OSM API):** Searches OpenStreetMap via a fast French mirror to map nearby supermarkets, gyms, parks, hospitals, and doctors within walking distance.
*   **AI Neighborhood "Vibes" (Gemini):** Pre-fetches postcode districts to batch-query Gemini for area safety evaluations, 3-word summaries, and 1-10 "vibe scores."
*   **Cache Partitioning & Instant Loads:** Employs smart cache partitioning to completely bypass network threads for fully cached properties, rendering them instantly on the dashboard.
*   **Unified TOML Configuration:** A clean, centralized `config.toml` system replacing hardcoded scripts, environment variables, and interactive prompts. Manage your commute coordinates, scoring weights, API settings, and custom Gemini criteria in one file.
*   **Smart Multi-Weighted Scoring (0-100):** Aggregates Price, Commute, Vibe, and Freshness into a unified score. The score is strictly set to `N/A` if critical parameters like Price, Commute, or Vibe are missing.
*   **Relative Price Dots:** Dynamic green-to-red color indicator showing how cheap or expensive a flat is relative to all other search results.
*   **Interactive Dashboard:** A local web server (`http://localhost:8888`) featuring progressive real-time loading, star/trash inbox triage, persistent inline text notes, and URL sorting.
*   **Fast Instant Termination:** Hit **`Ctrl+C`** at any time to instantly kill the entire script and background threads.

---

## 🚀 Setup & Installation

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/itsmuaaz/rightmove-lettings-triager.git
cd rightmove-lettings-triager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Settings & Credentials
On your first run, the script will automatically generate a `config.toml` file in the root directory based on the template. You can open this file to configure:
- **`work_latitude` / `work_longitude`**: Your office or POI coordinates.
- **`scoring.weights`**: The weighting used for the Smart Score algorithm.
- **`api.gemini`**: Define your custom AI "Vibe" criteria to personalize evaluations.
- *...and much more!*

*(Optional)* You can override API credentials dynamically by creating a `.env` file:
```env
TFL_APP_ID=your_tfl_app_id
TFL_APP_KEY=your_tfl_app_key
```

### 3. Run the Script
Execute the script using your Rightmove search URL:
```bash
python rightmove_search.py "YOUR_RIGHTMOVE_URL"
```
Open **`http://localhost:8888`** in your browser and watch properties enrich progressively in real-time!

---

## 🧪 Running Tests
The codebase comes with **193 automated unit and integration tests**:
```bash
pytest
```
