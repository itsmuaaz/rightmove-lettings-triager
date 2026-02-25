from calculator import CommuteCalculator
from tfl_client import TflClient
from reporter import Reporter
from config import load_config
import re

def main():
    config = load_config()
    client = TflClient(app_id=config['TFL_APP_ID'], app_key=config['TFL_APP_KEY'])
    destination = (51.5033, -0.1118) # Waterloo
    calculator = CommuteCalculator(tfl_client=client, destination=destination)
    
    prop = {
        'id': 'full-flow-prop',
        'address': 'Westminster',
        'location': {'latitude': 51.5007, 'longitude': -0.1246},
        '_original': {'location': {'latitude': 51.5007, 'longitude': -0.1246}},
        'price': '£1000 pcm'
    }
    
    print("Step 1: Calculating Commute...")
    try:
        res = calculator.calculate(prop['_original'])
        
        # Enrich property with result (as rightmove_search.py does)
        prop['commute_time'] = res['commute_time']
        prop['commute_fares'] = res.get('commute_fares')
        prop['commute_cycling'] = res.get('commute_cycling')
        
        print(f"Commute: {prop['commute_time']} mins")
        print(f"Fares: {prop['commute_fares']}")
        
        if not prop['commute_fares']:
             print("WARNING: No fares returned from API (check keys/time). Skipping HTML check.")
             return

        print("Step 2: Generating Report...")
        reporter = Reporter()
        html = reporter.generate_report([prop])
        
        print("Step 3: Checking HTML...")
        
        # Determine expected string logic based on reporter.py
        fares = prop['commute_fares']
        expected_str = ""
        peak = fares.get('peak')
        off_peak = fares.get('off_peak')
        total_cost = fares.get('total_cost')
        cost = fares.get('cost')
        
        if peak and off_peak:
            expected_str = f"£{peak/100:.2f} / £{off_peak/100:.2f}"
        elif total_cost:
            expected_str = f"£{total_cost/100:.2f}"
        elif cost:
            expected_str = f"£{cost/100:.2f}"
            
        if expected_str and (expected_str in html or expected_str.replace('£', '&#163;') in html):
            print(f"SUCCESS: Found expected fare '{expected_str}' in HTML report!")
        else:
            print(f"ERROR: Expected '{expected_str}' not found in HTML.")
            # Print context around "min"
            match = re.search(r'min(.*?)</div>', html, re.DOTALL)
            if match:
                 print(f"Context: {match.group(1).strip()}")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
