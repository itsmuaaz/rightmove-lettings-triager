# Rightmove Lettings Triager 🏡🚇📊

An automated, intelligent, and highly interactive property search, evaluation, and triage tool for the London rental market. It fetches search listings directly from Rightmove, enriches them with multi-modal commute times, local amenities, and AI-powered neighborhood vibes, and serves them up in a beautiful, responsive, stateful HTML dashboard.

![Rightmove Lettings Triager Dashboard](./screenshot.png)

---

## 🌟 Core Features

### 1. Automated Scraping & Auto-Pagination
Simply supply page 1 of any Rightmove search URL. The tool dynamically extracts the total results count and automatically paginates through every single page to parse all listings.

### 2. Multi-Modal Commute Calculations (TfL API)
Calculates real-world **Public Transport** and **Cycling** travel times to your specific workplace using the official Transport for London (TfL) Unified API.
*   **Tuesday 9:00 AM Benchmark:** All commute queries are standardized to the next upcoming Tuesday at 9:00 AM to ensure travel times are consistent and not affected by when you run the script (e.g. weekend schedules).
*   **Fares Integration:** Automatically retrieves and estimates the single journey Peak/Off-Peak ticket cost.

### 3. OpenStreetMap Amenity Detection (Overpass API)
Scans OpenStreetMap using a highly optimized French Overpass mirror to identify nearby **Supermarkets, Gyms, Parks, and Healthcare facilities (Hospitals/Doctors)** within a custom radius.

### 4. AI-Powered Neighborhood "Vibes" (Google Gemini)
Pre-fetches and batches neighborhood postcode districts to query Google Gemini, generating a qualitative summary, keywords, safety evaluation, and a 1-10 "vibe score."

### 5. Smart Multi-Weighted Scoring System
Calculates an aggregate **Smart Score (0-100)** for every flat based on user-adjustable weights for **Price, Commute, Vibe, and Freshness**. Adjust weights dynamically via a CLI prompt on startup. If critical parameters like Price, Commute, or Vibe are missing or unprocessed, the score is strictly set to `N/A`.

### 6. Interactive, Stateful HTML Dashboard
Serves a local web server (default port `8888`) with a modern, responsive design and advanced interactive features:
*   **Inbox Triage:** Click **Star** to move properties to the collapsible "Shortlisted Properties" grid. Click **Trash** to hide/dismiss properties.
*   **State Persistence:** Viewed, shortlisted, and dismissed states are tracked locally in `history.json` and persist across runs.
*   **Persistent Inline Notes:** Write custom notes directly on any property card; they save automatically to `notes.json` on the fly.
*   **Relative Price Dots:** Visually displays a green-to-red gradient dot based on where the flat's price sits relative to the minimum and maximum prices of your search.
*   **Manual Commute Refresh:** Hover over transit times and click 🔄 to bypass the cache and force-trigger a fresh live query to TfL.
*   **Stateful URL Sorting:** Click table headers to sort instantly by Smart Score, Price, Vibe, or Commute Time (Force sort by Min, Transit, or Cycling). Sort query parameters are preserved in the URL for consistent refreshes.

---

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/itsmuaaz/rightmove-lettings-triager.git
cd rightmove-lettings-triager
```

### 2. Setup Virtual Environment & Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure API Credentials
Create a `.env` file in the root directory:
```env
TFL_APP_ID=your_tfl_app_id
TFL_APP_KEY=your_tfl_app_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key  # Optional fallback
```

### 4. Configure Your Work Location
To calculate commutes to your actual office, open `rightmove_search.py` and modify the coordinates in line 21 with your office's latitude and longitude:
```python
WORK_LOCATION_COORDS = (51.5349, -0.1238)  # Default: King's Cross area
```

---

## 🚀 How to Run

1.  Go to [Rightmove.co.uk](https://www.rightmove.co.uk/) and perform your search (set rent limits, bedrooms, location, etc.).
2.  **Copy the search URL** from your browser.
3.  Execute the script:
    ```bash
    python rightmove_search.py "YOUR_RIGHTMOVE_URL"
    ```
4.  The script will prompt you if you'd like to adjust the default scoring weights. Type **`n`** for default or **`y`** to customize.
5.  Open **`http://localhost:8888`** in your browser. 
6.  The dashboard supports **Progressive Loading**. Watch properties load instantly, and hit **"Refresh"** in the floating blue progress banner to see them enrich in real-time as background threads fetch TfL, OSM, and Gemini data!
7.  Press **`Ctrl+C`** in your terminal at any time to instantly stop the program.

---

## 🧪 Developer Section (Running Tests)
The project comes with an extensive automated test suite of **175 unit and integration tests** verifying caches, clients, and API integration.

To run the tests:
```bash
pytest
```
To run tests with coverage reporting:
```bash
pytest --cov=.
```
