import json
import re
from rightmove_search import parse_property_data

def verify_real_data():
    with open('verify_agencies.html', 'r', encoding='utf-8') as f:
        html = f.read()

    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
    
    if match:
        data = json.loads(match.group(1))
        properties = data['props']['pageProps']['searchResults']['properties']
        
        print(f"Found {len(properties)} properties to verify:")
        
        for p in properties:
            parsed = parse_property_data(p)
            print("-" * 20)
            print(f"Address: {parsed['address']}")
            print(f"Agency Name: '{parsed['agency_name']}'")
            print(f"Agency Phone: '{parsed['agency_phone']}'")
            
            # Basic validation
            if not parsed['agency_name']:
                print("WARNING: Agency Name is empty!")
            if not parsed['agency_phone']:
                print("WARNING: Agency Phone is empty!")

if __name__ == "__main__":
    verify_real_data()
