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
from config_manager import ConfigManager

def is_tfl_cached(tfl_client: TflClient, from_coords: tuple, to_coords: tuple) -> bool:
    """Checks if TfL cache has valid benchmarked data for both transport and cycling modes."""
    transit_hit = tfl_client.is_cached(from_coords, to_coords, "Public Transport")
    cycling_hit = tfl_client.is_cached(from_coords, to_coords, "Cycling")
    return transit_hit and cycling_hit

def is_osm_cached(amenity_calculator, lat: float, lon: float) -> bool:
    """Checks if OpenStreetMap amenity data is locally cached for the coordinates."""
    if not amenity_calculator or not amenity_calculator.amenity_client:
        return False
    return amenity_calculator.amenity_client.is_cached(lat, lon, amenity_calculator.radius)

def is_vibe_cached(vibe_client: VibeClient, location_key: str) -> bool:
    """Checks if the vibe score is locally cached and valid."""
    with vibe_client.lock:
        if location_key in vibe_client.cache:
            entry = vibe_client.cache[location_key]
            if isinstance(entry, dict) and entry.get("cached_at"):
                # Fast bypass check: If it exists and has a timestamp, we consider it cached for partitioning purposes.
                # Actual TTL stale check happens inside vibe_client.get_vibes during the synchronous fetch.
                return True
    return False

def is_fully_cached(tfl_client, amenity_calculator, vibe_client, property_data, work_coords):
    """Unified check to determine if a property's dynamic metrics are entirely cached."""
    # Check TfL
    lat, lon = property_data.get('latitude'), property_data.get('longitude')
    if not lat or not lon:
        return False
    
    if not is_tfl_cached(tfl_client, (lat, lon), work_coords):
        return False
        
    # Check Amenities
    if not is_osm_cached(amenity_calculator, lat, lon):
        return False
        
    # Check Vibe
    vibe_loc = extract_location_for_vibe(property_data.get('displayAddress', property_data.get('address', '')), (lat, lon))
    if not vibe_loc or not is_vibe_cached(vibe_client, vibe_loc):
        return False
        
    return True

def populate_property_sync(p):
    """Synchronously populates a property using only local cache data. No thread pools or locks needed."""
    global calculator, amenity_calculator, note_manager, history_manager, vibe_client

    try:
        if calculator:
            res = calculator.calculate(p['_original'])
            p['distance'] = res['distance']
            p['commute_time'] = res['commute_time']
            p['commute_fares'] = res.get('commute_fares')
            p['commute_cycling'] = res.get('commute_cycling')

        if amenity_calculator:
            p['nearby_amenities'] = amenity_calculator.calculate(p.get('latitude'), p.get('longitude'))

        if vibe_client:
            location_key = extract_location_for_vibe(p['address'], (p.get('latitude'), p.get('longitude')))
            if location_key:
                vibes = vibe_client.get_vibes([location_key])
                p['vibe'] = vibes.get(location_key)

        if note_manager:
            p['note'] = note_manager.get_note(p['id'])

        if history_manager:
            p['history_status'] = history_manager.get_status(p['id'])
    except Exception as e:
        sys.stderr.write(f"Error sync-processing property {p.get('id')}: {e}\n")

    return p

# Global references for testing purposes (in a real app, use dependency injection)
calculator = None
amenity_calculator = None
note_manager = None
history_manager = None
search_state = None
vibe_client = None

def print_dashboard_banner(url, stage="startup"):
    """Prints a decorated banner for the dashboard URL."""
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    w = 52 # Inner width
    
    print(f"\n  {CYAN}╔{'═' * w}╗{RESET}")
    print(f"  {CYAN}║{' ' * w}║{RESET}")
    
    if stage == "startup":
        title = "🚀  DASHBOARD RUNNING"
        # Adjust padding for emoji visual width (2 chars vs len 1)
        pad = w - len(title) - 3 - 1 
        print(f"  {CYAN}║{RESET}   {BOLD}{title}{RESET}{' ' * pad}{CYAN}║{RESET}")
        
        print(f"  {CYAN}║{' ' * w}║{RESET}")
        msg = "Access your results at:"
        print(f"  {CYAN}║{RESET}   {msg.ljust(w-3)}{CYAN}║{RESET}")
        
        print(f"  {CYAN}║{RESET}   {BOLD}{url}{RESET}{' ' * (w - 3 - len(url))}{CYAN}║{RESET}")
        
        print(f"  {CYAN}║{' ' * w}║{RESET}")
        print(f"  {CYAN}║{RESET}   {'(Press Ctrl+C to stop)'.ljust(w-3)}{CYAN}║{RESET}")

    else:
        title = "✅  PROCESSING COMPLETE"
        pad = w - len(title) - 3 - 1
        print(f"  {CYAN}║{RESET}   {BOLD}{title}{RESET}{' ' * pad}{CYAN}║{RESET}")
        
        print(f"  {CYAN}║{' ' * w}║{RESET}")
        msg = "View final results at:"
        print(f"  {CYAN}║{RESET}   {msg.ljust(w-3)}{CYAN}║{RESET}")
        
        print(f"  {CYAN}║{RESET}   {BOLD}{url}{RESET}{' ' * (w - 3 - len(url))}{CYAN}║{RESET}")

    print(f"  {CYAN}║{' ' * w}║{RESET}")
    print(f"  {CYAN}╚{'═' * w}╝{RESET}\n")

def fetch_data(url, user_agent):
    """Fetch the page HTML using curl."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", user_agent, url],
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
    
    # Extract detailed agency info
    customer = p.get('customer', {})
    agency_name = customer.get('branchDisplayName') or customer.get('brandTradingName') or ""
    agency_phone = customer.get('contactTelephone') or ""
    
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
        'agency_name': agency_name,
        'agency_phone': agency_phone,
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
            location_key = extract_location_for_vibe(p['address'], (p.get('latitude'), p.get('longitude')))
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
    # Default to smart_score descending (handle None scores gracefully)
    properties.sort(key=lambda x: x.get('smart_score') if x.get('smart_score') is not None else -1.0, reverse=True)

    return properties

def configure_scoring():
    """Interactively configure scoring weights."""
    defaults = {
        "price": 0.3,
        "commute": 0.3,
        "vibe": 0.3,
        "freshness": 0.1
    }
    manager = ConfigManager(config_file=".scoring_config.json", defaults=defaults)
    current_weights = manager.load_config()
    
    print("\nCurrent Scoring Weights:")
    for k, v in current_weights.items():
        print(f"  - {k.capitalize()}: {v*100:.0f}%")
        
    choice = input("\nDo you want to change these scoring weights? (y/n) [n]: ").lower().strip()
    if choice != 'y':
        return

    print("\nEnter new weights (0-100). They will be normalized to sum to 100%.")
    new_weights = {}
    for key in ["price", "commute", "vibe", "freshness"]:
        while True:
            val = input(f"  {key.capitalize()}: ")
            try:
                val_float = float(val)
                if val_float < 0:
                    print("    Please enter a non-negative number.")
                    continue
                new_weights[key] = val_float
                break
            except ValueError:
                print("    Invalid input. Please enter a number.")
    
    manager.save_config(new_weights)
    print("New weights saved.\n")

def main():
    """Main execution function to search properties and generate reports."""
    # Define globals
    global calculator, amenity_calculator, note_manager, history_manager, search_state, vibe_client, config

    config_manager = ConfigManager("config.toml")
    config = config_manager.load_config()

    parser = argparse.ArgumentParser(description="Search Rightmove properties and calculate commutes/amenities.")
    parser.add_argument("url", help="The Rightmove search results URL.")
    parser.add_argument("--radius", type=int, default=1000, help="Search radius for amenities in meters (default: 1000).")
    parser.add_argument("--port", type=int, default=8888, help="Port to run the dashboard server on (default: 8888).")
    parser.add_argument("--no-server", action="store_true", help="Skip starting the dashboard server.")
    args = parser.parse_args()

    configure_scoring()

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
        
        html = fetch_data(url, config.get('network', {}).get('user_agent', 'Mozilla/5.0'))
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
    credentials = config.get('credentials', {})
    tfl = TflClient(app_id=credentials.get('tfl_app_id'), app_key=credentials.get('tfl_app_key'))
    
    # Run Automated Cache Cleanup Chore
    from tfl_client import cleanup_stale_caches
    cleanup_stale_caches(tfl.cache_dir)
    
    work_coords = (config.get('search', {}).get('work_latitude', 51.5349), config.get('search', {}).get('work_longitude', -0.1238))
    calculator = CommuteCalculator(tfl_client=tfl, destination=work_coords)
    
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
        print_dashboard_banner(f"http://localhost:{port}", "startup")
        sys.stderr.write("Search continues in background...\n")

    sys.stderr.write(f"Calculating metrics for {len(all_properties)} properties...\n")

    # ---- PARTITIONING PASS ----
    synchronous_properties = []
    async_properties = []

    for p in all_properties:
        if is_fully_cached(tfl, amenity_calculator, vibe_client, p, work_coords):
            synchronous_properties.append(p)
        else:
            async_properties.append(p)

    if synchronous_properties:
        sys.stderr.write(f"Instantly loading {len(synchronous_properties)} fully cached properties...\n")
        for p in synchronous_properties:
            populate_property_sync(p)
        search_state.processed += len(synchronous_properties)

    if async_properties:
        # Pre-fetch Vibes for async locations to batch API calls
        locations = set()
        for p in async_properties:
            loc = extract_location_for_vibe(p['address'], (p.get('latitude'), p.get('longitude')))
            if loc:
                locations.add(loc)

        if locations:
            vibe_client.get_vibes(list(locations))

        sys.stderr.write(f"Querying external APIs for remaining {len(async_properties)} properties...\n")
        # Using 3 workers to stay well within TfL's 50 req/min limit and Overpass limits
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        futures = [executor.submit(process_property, p, i, len(async_properties))
                   for i, p in enumerate(async_properties)]

        try:
            # Wait for all to complete using a non-blocking loop so KeyboardInterrupt (Ctrl+C) can be processed instantly
            import time
            while any(not f.done() for f in futures):
                time.sleep(0.1)
        except KeyboardInterrupt:
            sys.stderr.write("\n\nProcess interrupted by user (Ctrl+C). Exiting immediately...\n")
            executor.shutdown(wait=False)
            import os
            os._exit(1)
        finally:
            executor.shutdown(wait=True)
    else:
        sys.stderr.write("All properties loaded from cache! Bypassing thread pool entirely.\n")

    # Calculate Smart Scores and Sort
    sys.stderr.write("Calculating Smart Scores...\n")
    all_properties = post_process_properties(all_properties)
    
    # Mark as complete
    search_state.status = "complete"
    
    print_dashboard_banner(f"http://localhost:{port}", "completion")

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
