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

# Configuration
WORK_LOCATION_COORDS = (51.5349, -0.1238)  # N1C 4AG (Work)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

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
    published_on = p.get('firstPublishedDate')
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

def get_sort_key(p):
    """Determine the sort key for a property based on shortest commute."""
    commute = p.get('commute_time')
    cycling = p.get('commute_cycling')
    
    if commute is None and cycling is None:
        return float('inf')
    
    if commute is None:
        return cycling
    
    if cycling is None:
        return commute
        
    return min(commute, cycling)

def main():
    """Main execution function to search properties and generate reports."""
    parser = argparse.ArgumentParser(description="Search Rightmove properties and calculate commutes/amenities.")
    parser.add_argument("url", help="The Rightmove search results URL.")
    parser.add_argument("--radius", type=int, default=1000, help="Search radius for amenities in meters (default: 1000).")
    parser.add_argument("--port", type=int, default=8888, help="Port to run the dashboard server on (default: 8888).")
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
    
    # Initialize history for new properties
    history_manager.initialize_properties(all_properties)

    sys.stderr.write(f"Calculating metrics for {len(all_properties)} properties...\n")

    # Calculate commute, distance and amenities in parallel
    def process_property(p, i, total):
        sys.stderr.write(f"[{i+1}/{total}] Processing: {p['address'][:40]}...\n")
        # CommuteCalculator.calculate now parallelizes public/cycling calls
        res = calculator.calculate(p['_original'])
        p['distance'] = res['distance']
        p['commute_time'] = res['commute_time']
        p['commute_cycling'] = res.get('commute_cycling')
        
        # Amenity calculation
        p['nearby_amenities'] = amenity_calculator.calculate(p.get('latitude'), p.get('longitude'))
        
        # Inject notes
        p['note'] = note_manager.get_note(p['id'])
        
        # Inject history status
        p['history_status'] = history_manager.get_status(p['id'])
        
        return p

    # Using 3 workers to stay well within TfL's 50 req/min limit and Overpass limits
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(process_property, p, i, len(all_properties)) 
                   for i, p in enumerate(all_properties)]
        # Wait for all to complete
        concurrent.futures.wait(futures)
    
    # Sort by shortest commute (default)
    all_properties.sort(key=get_sort_key)

    # Generate Markdown Report (Still useful for quick viewing)
    reporter = Reporter()
    md_content = reporter.generate_markdown(all_properties, for_html=False)
    
    with open('results.md', 'w') as f:
        f.write(md_content)
        
    # Generate HTML Report for Dashboard
    md_for_html = reporter.generate_markdown(all_properties, for_html=True)
    html_content = reporter.convert_to_html(md_for_html)
    
    # Start Dashboard Server
    sys.stderr.write(f"Starting dashboard on http://localhost:{port}\n")
    sys.stderr.write("Press Ctrl+C to stop.\n")
    
    socketserver.TCPServer.allow_reuse_address = True
    server = HTTPServer(('127.0.0.1', port), DashboardHandler)
    server.html_content = html_content
    server.note_manager = note_manager
    server.history_manager = history_manager
    server.properties = all_properties
    server.reporter = reporter
    server.tfl_client = tfl
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.server_close()

if __name__ == "__main__":
    main()
