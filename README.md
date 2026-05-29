# Rightmove Lettings Triager 🏡🚇📊

Automates the tedious process of finding London rentals. It scrapes Rightmove, enriches listings with TfL commute times, local amenities (OpenStreetMap), and AI-generated neighborhood "vibes" (Gemini), then presents them in a stateful, interactive dashboard.

> 💡 **PRO TIP:** Set up Rightmove **Email Alerts** for your search. When an alert arrives, paste the URL into this script. The built-in **History Manager** hides flats you've already dismissed/viewed, highlighting only new listings!

![Dashboard](./screenshot.png)

## 🎯 How It Works: Leverage Native Filters

We didn't build custom filters (like price range, bedrooms, or property type) because Rightmove already does this perfectly. **Set up your search directly on Rightmove with all your desired filters**, copy the resulting URL, and feed it to the script. The script uses that exact link to pull your tailored results.

**Example Usage:**
```bash
python rightmove_search.py "https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=N1C+4AG&useLocationIdentifier=true&locationIdentifier=POSTCODE%5E4475720&radius=3.0&propertyTypes=flat&minBedrooms=2&maxPrice=2750&minPrice=2250&maxBedrooms=2&_includeLetAgreed=on&index=0&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=undefined&furnishTypes=furnished&minBathrooms=2"
```

## ✨ Core Features
*   **Auto-Scraping:** Processes all result pages from your Rightmove URL.
*   **Stateful Triage:** Tracks flats as `New`, `Viewed`, `Shortlisted`, or `Dismissed` across sessions.
*   **TfL Commute:** Precise public transport and cycling times (standardized to Tuesday 9:00 AM) + fare costs.
*   **Amenities:** Proximity to supermarkets, gyms, parks, etc., via OpenStreetMap.
*   **AI "Vibes":** Area safety and lifestyle evaluations powered by Gemini.
*   **Smart Scoring (0-100):** Ranks properties based on your custom weighting of Price, Commute, Vibe, and Freshness.
*   **Interactive Dashboard:** Real-time loading, persistent notes, and triage controls at `http://localhost:8888`.
*   **Instant Loads:** Fully cached properties render immediately, bypassing network delays.

## 🚀 Quick Start

**1. Install**
Requires **Python 3.11+** and the Google Gemini CLI configured.
```bash
git clone https://github.com/itsmuaaz/rightmove-lettings-triager.git
cd rightmove-lettings-triager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Configure**
Run the script once to generate `config.toml`. Edit it to set:
*   `work_latitude` / `work_longitude` (Your office coordinates)
*   `scoring.weights`
*   `api.gemini` (Custom vibe criteria)

*(Optional)* Create a `.env` file for TfL API keys for higher rate limits (works anonymously without them).

**3. Run**
Execute the script using your custom filtered Rightmove URL. Then, open **`http://localhost:8888`** and start triaging!

---
**Tests:** Run `pytest` to execute the 193 automated tests.
