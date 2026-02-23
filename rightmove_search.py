import json
import re
import sys
import math
import subprocess
import argparse
import concurrent.futures
from http.server import HTTPServer
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

# ... (existing functions fetch_data, extract_json_data, update_url_index, parse_property_data, get_sort_key) ...

def main():
    """Main execution function to search properties and generate reports."""
    parser = argparse.ArgumentParser(description="Search Rightmove properties and calculate commutes/amenities.")
    parser.add_argument("url", help="The Rightmove search results URL.")
    parser.add_argument("--radius", type=int, default=1000, help="Search radius for amenities in meters (default: 1000).")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the dashboard server on (default: 8000).")
    args = parser.parse_args()

    # ... (fetching logic) ...

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
        # ... (metric calculation) ...
        
        # Inject notes
        p['note'] = note_manager.get_note(p['id'])
        
        # Inject history status
        p['history_status'] = history_manager.get_status(p['id'])
        
        return p

    # ... (parallel execution) ...
    
    # ... (sorting) ...

    # Generate Markdown Report (Still useful for quick viewing)
    reporter = Reporter()
    # ... (markdown generation) ...
    
    # Start Dashboard Server
    sys.stderr.write(f"Starting dashboard on http://localhost:{port}\n")
    sys.stderr.write("Press Ctrl+C to stop.\n")
    
    server = HTTPServer(('127.0.0.1', port), DashboardHandler)
    server.html_content = html_content
    server.note_manager = note_manager
    server.history_manager = history_manager
    server.properties = all_properties
    server.reporter = reporter
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.server_close()

if __name__ == "__main__":
    main()
