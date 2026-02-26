import json
import re
import sys
import math
import subprocess
import argparse
import concurrent.futures
from http.server import HTTPServer
import socketserver
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from config import load_config
from tfl_client import TflClient
from calculator import CommuteCalculator
from reporter import Reporter
from amenity_client import AmenityClient
from amenity_calculator import AmenityCalculator
from notes_manager import NoteManager
from dashboard import DashboardHandler
from history_manager import HistoryManager
from search_state import SearchState
from vibe_client import VibeClient
import threading
import time
from utils import get_sort_key, extract_postcode_district, extract_location_for_vibe, extract_numeric_price
from scoring import SmartScorer

# Configuration
WORK_LOCATION_COORDS = (51.5349, -0.1238)  # N1C 4AG (Work)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Global references for testing purposes (in a real app, use dependency injection)
calculator = None
amenity_calculator = None
note_manager = None
history_manager = None
search_state = None
vibe_client = None

def fetch_data(url):
    """Fetch the page HTML using curl."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", USER_AGENT, url],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        sys.stderr.write(f"Error fetching data: {str(e)}\n")
        return None

def extract_json_data(html):
    """Extract the __NEXT_DATA__ JSON blob from the HTML."""
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except Exception as e:
        sys.stderr.write(f"Error parsing JSON: {str(e)}\n")
        return None

def update_url_index(url, new_index):
    """Update the 'index' parameter in the URL."""
    u = urlparse(url)
    query = parse_qs(u.query)
    query['index'] = [str(new_index)]
    new_query = urlencode(query, doseq=True)
    return urlunparse(u._replace(query=new_query))

def parse_property_data(p):
    """Extract relevant fields from a raw property object."""
    prop_id = str(p.get('id', ''))
    price = p.get('price', {}).get('displayPrices', [{'displayPrice': 'N/A'}])[0]['displayPrice']
    prop_type = p.get('propertyTypeFullDescription', 'Property')
    address = p.get('displayAddress', 'No Address')
    agent = p.get('customer', {}).get('brandTradingName', 'Unknown')
    url = p.get('propertyUrl', '')
    
    # New fields
    image_url = None
    images = p.get('propertyImages', {}).get('images', [])
    if images:
        image_url = images[0].get('srcUrl')
        
    bedrooms = p.get('bedrooms', 0)
    
    # Date extraction logic: Collect all potential dates and pick the latest one
    potential_dates = []
    
    fv_date = p.get('firstVisibleDate')
    if fv_date:
        potential_dates.append(fv_date)
        
    lu_date = p.get('listingUpdate', {}).get('listingUpdateDate')
    if lu_date:
        potential_dates.append(lu_date)
        
    fp_date = p.get('firstPublishedDate')
    if fp_date:
        potential_dates.append(fp_date)
        
    if potential_dates:
        # Sort descending (latest first)
        published_on = sorted(potential_dates, reverse=True)[0]
    else:
        published_on = None
        
    summary = p.get('summary', '')
    
    location = p.get('location', {})
    latitude = location.get('latitude')
    longitude = location.get('longitude')

    return {
        'id': prop_id,
        'price': price,
        'type': prop_type,
        'address': address,
        'agent': agent,
        'url': url,
        'image_url': image_url,
        'bedrooms': bedrooms,
        'published_on': published_on,
        'summary': summary,
        'latitude': latitude,
        'longitude': longitude,
        '_original': p # Keep raw data for calculator
    }

def process_property(p, i, total):
    """Process a single property: calculate metrics, amenities, and vibe."""
    # Use global dependencies (not ideal but works for this script structure)
    global calculator, amenity_calculator, note_manager, history_manager, search_state, vibe_client
    
    sys.stderr.write(f"[{i+1}/{total}] Processing: {p['address'][:40]}...\n")
    try:
        # CommuteCalculator.calculate now parallelizes public/cycling calls
        if calculator:
            res = calculator.calculate(p['_original'])
            p['distance'] = res['distance']
            p['commute_time'] = res['commute_time']
            p['commute_fares'] = res.get('commute_fares')
            p['commute_cycling'] = res.get('commute_cycling')
        
        # Amenity calculation
        if amenity_calculator:
            p['nearby_amenities'] = amenity_calculator.calculate(p.get('latitude'), p.get('longitude'))
        
        # Vibe calculation
        if vibe_client:
            location_key = extract_location_for_vibe(p['address'])
            if location_key:
                vibes = vibe_client.get_vibes([location_key])
                p['vibe'] = vibes.get(location_key)
        
        # Inject notes
        if note_manager:
            p['note'] = note_manager.get_note(p['id'])
        
        # Inject history status
        if history_manager:
            p['history_status'] = history_manager.get_status(p['id'])
    except Exception as e:
        sys.stderr.write(f"Error processing property {p.get('id')}: {e}\n")
    finally:
        if search_state:
            search_state.processed += 1
    
    return p

def post_process_properties(properties):
    """
    Enrich properties with Smart Score.
    1. Calculate global Min/Max Price.
    2. Calculate Score for each property.
    3. Sort properties by Score (Descending).
    """
    if not properties:
        return properties

    # 1. Global Stats
    valid_prices = []
    for p in properties:
        val = extract_numeric_price(p.get('price'))
        if val is not None:
            valid_prices.append(val)
    
    global_stats = {
        "min_price": min(valid_prices) if valid_prices else None,
        "max_price": max(valid_prices) if valid_prices else None
    }

    # 2. Scoring
    scorer = SmartScorer()
    for p in properties:
        score_result = scorer.calculate_score(p, global_stats)
        p['smart_score'] = score_result['total']
        p['score_breakdown'] = score_result['breakdown']

    # 3. Sorting
    # Default to smart_score descending
    properties.sort(key=lambda x: x.get('smart_score', 0), reverse=True)

    return properties

def main():
    """Main execution function to search properties and generate reports."""
    # Define globals
    global calculator, amenity_calculator, note_manager, history_manager, search_state, vibe_client

    parser = argparse.ArgumentParser(description="Search Rightmove properties and calculate commutes/amenities.")
    parser.add_argument("url", help="The Rightmove search results URL.")
    parser.add_argument("--radius", type=int, default=1000, help="Search radius for amenities in meters (default: 1000).")
    parser.add_argument("--port", type=int, default=8888, help="Port to run the dashboard server on (default: 8888).")
    parser.add_argument("--no-server", action="store_true", help="Skip starting the dashboard server.")
    args = parser.parse_args()

    base_url = args.url
    radius = args.radius
    port = args.port
    
    all_properties = []
    current_index = 0
    total_results = None
    per_page = 24 # Default Rightmove page size

    sys.stderr.write("Starting search and auto-pagination...\n")

    while True:
        url = update_url_index(base_url, current_index)
        sys.stderr.write(f"Fetching index {current_index}...\n")
        
        html = fetch_data(url)
        if not html:
            break
            
        data = extract_json_data(html)
        if not data:
            sys.stderr.write("Failed to find data on page. Stopping.\n")
            break

        page_props = data.get('props', {}).get('pageProps', {})
        search_results = page_props.get('searchResults', {})
        
        # On first page, get total count
        if total_results is None:
            try:
                total_results = int(search_results.get('resultCount', 0))
                per_page = int(search_results.get('searchParameters', {}).get('numberOfPropertiesPerPage', 24))
                sys.stderr.write(f"Total results to fetch: {total_results}\n")
            except:
                total_results = 0

        props = search_results.get('properties', [])
        if not props:
            break
            
        # Parse and store
        for p in props:
            parsed = parse_property_data(p)
            all_properties.append(parsed)
        
        # Check if we have more pages
        current_index += per_page
        if current_index >= total_results:
            break

    if not all_properties:
        print("No properties found.")
        return

    # Initialize calculators and storage
    config = load_config()
    tfl = TflClient(app_id=config.get('TFL_APP_ID'), app_key=config.get('TFL_APP_KEY'))
    calculator = CommuteCalculator(tfl_client=tfl, destination=WORK_LOCATION_COORDS)
    
    amenity_client = AmenityClient()
    amenity_calculator = AmenityCalculator(amenity_client=amenity_client, radius=radius)
    
    note_manager = NoteManager()
    history_manager = HistoryManager()
    
    vibe_client = VibeClient()

    # Initialize history for new properties
    history_manager.initialize_properties(all_properties)

    # Initialize Shared Search State
    search_state = SearchState(
        properties=all_properties,
        total=len(all_properties),
        processed=0,
        status="processing"
    )
    
    reporter = Reporter()
    server_thread = None

    # Start Server in Background Thread
    if not args.no_server:
        sys.stderr.write(f"Starting dashboard on http://localhost:{port}\n")
        
        def run_server():
            socketserver.TCPServer.allow_reuse_address = True
            try:
                server = HTTPServer(('127.0.0.1', port), DashboardHandler)
                # Inject dependencies
                server.search_state = search_state
                server.note_manager = note_manager
                server.history_manager = history_manager
                server.reporter = reporter
                server.tfl_client = tfl
                server.serve_forever()
            except OSError as e:
                sys.stderr.write(f"Error starting server: {e}\n")
            except Exception as e:
                sys.stderr.write(f"Server runtime error: {e}\n")

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        sys.stderr.write("Dashboard running. Search continues in background...\n")

    sys.stderr.write(f"Calculating metrics for {len(all_properties)} properties...\n")
    
    # Pre-fetch Vibes for all locations to batch API calls
    locations = set()
    for p in all_properties:
        loc = extract_location_for_vibe(p['address'])
        if loc:
            locations.add(loc)
    
    if locations:
        sys.stderr.write(f"Prefetching vibes for {len(locations)} locations...\n")
        vibe_client.get_vibes(list(locations))

    # Using 3 workers to stay well within TfL's 50 req/min limit and Overpass limits
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(process_property, p, i, len(all_properties)) 
                   for i, p in enumerate(all_properties)]
        # Wait for all to complete
        concurrent.futures.wait(futures)
    
    # Calculate Smart Scores and Sort
    sys.stderr.write("Calculating Smart Scores...\n")
    all_properties = post_process_properties(all_properties)
    
    # Mark as complete
    search_state.status = "complete"

    # Generate HTML Report for Dashboard
    html_content = reporter.generate_report(all_properties, processed_count=len(all_properties), total_count=len(all_properties))
    
    # Save HTML report to file (useful for debugging/offline)
    with open('results.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Keep server running if requested
    if not args.no_server and server_thread:
        sys.stderr.write("Processing complete. Server still running. Press Ctrl+C to stop.\n")
        try:
            server_thread.join()
        except KeyboardInterrupt:
             print("\nStopping.")
    else:
        sys.stderr.write("Reports generated in results.html\n")

if __name__ == "__main__":
    main()
