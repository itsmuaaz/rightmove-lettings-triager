from calculator import CommuteCalculator
from tfl_client import TflClient
from config import load_config

def main():
    config = load_config()
    client = TflClient(app_id=config['TFL_APP_ID'], app_key=config['TFL_APP_KEY'])
    # From Westminster to Waterloo (should be cyclable)
    destination = (51.5033, -0.1118) # Waterloo
    
    calculator = CommuteCalculator(tfl_client=client, destination=destination)
    
    # Dummy Property
    # We pass a dict that looks like the raw property data
    prop = {
        'location': {
            'latitude': 51.5007,
            'longitude': -0.1246
        }
    }
    
    print("Calculating commute for property...")
    try:
        result = calculator.calculate(prop)
        print("--- Result ---")
        print(f"Time: {result.get('commute_time')} mins")
        print(f"Cycling: {result.get('commute_cycling')} mins")
        print(f"Fares: {result.get('commute_fares')}")
        
        fares = result.get('commute_fares', {})
        if fares and ('peak' in fares or 'off_peak' in fares or 'total_cost' in fares):
            print("SUCCESS: Fares propagated!")
        else:
            print("WARNING: No fares in result.")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
