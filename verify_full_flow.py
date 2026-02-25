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
    
    # Lithos Road, NW3
    prop = {
        'id': 'lithos-road',
        'address': 'Lithos Road, NW3',
        'location': {'latitude': 51.5491, 'longitude': -0.1823},
        '_original': {'location': {'latitude': 51.5491, 'longitude': -0.1823}},
        'price': '£1000 pcm'
    }
    
    print("Step 1: Calculating Commute for Lithos Road...")
    try:
        res = calculator.calculate(prop['_original'])
        
        # Enrich property with result
        prop['commute_time'] = res['commute_time']
        prop['commute_fares'] = res.get('commute_fares')
        prop['commute_cycling'] = res.get('commute_cycling')
        
        print(f"Commute: {prop['commute_time']} mins")
        print(f"Fares: {prop['commute_fares']}")
        
        print("Step 2: Generating Report...")
        reporter = Reporter()
        html = reporter.generate_report([prop])
        
        print("Step 3: Checking HTML...")
        
        # With the fix, we expect the cost of the FASTEST route.
        # Based on debug output, Fastest (36m) is £5.35 (Peak) / £4.85 (OffPeak)
        # But wait, TflClient uses 'timeIs': 'Arriving', 'time': '0900'.
        # The debug output used the same params.
        
        fares = prop['commute_fares']
        if not fares:
            print("ERROR: No fares returned.")
            return

        expected_str = ""
        peak = fares.get('peak')
        off_peak = fares.get('off_peak')
        
        if peak and off_peak:
            expected_str = f"£{peak/100:.2f} / £{off_peak/100:.2f}"
            
        if expected_str and (expected_str in html or expected_str.replace('£', '&#163;') in html):
            print(f"SUCCESS: Found expected fare '{expected_str}' in HTML report!")
        else:
            print(f"ERROR: Expected '{expected_str}' not found in HTML.")
            # Print context
            match = re.search(r'min(.*?)</div>', html, re.DOTALL)
            if match:
                 print(f"Context: {match.group(1).strip()}")
            
    except Exception as e:
        print(f"ERROR: {e}")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
