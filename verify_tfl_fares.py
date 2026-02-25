from tfl_client import TflClient
from config import load_config

def main():
    config = load_config()
    client = TflClient(app_id=config['TFL_APP_ID'], app_key=config['TFL_APP_KEY'])
    
    # From Westminster to Canary Wharf
    from_coords = (51.5007, -0.1246)
    to_coords = (51.5045, 0.0135) # Near Canary Wharf
    
    print("Fetching journey data from Westminster to Canary Wharf...")
    try:
        data = client.get_journey_data(from_coords, to_coords)
        if data:
            print("\n--- Journey Data ---")
            print(f"Duration: {data.get('duration')} minutes")
            print(f"Fares: {data.get('fares')}")
            
            fares = data.get('fares', {})
            if 'peak' in fares or 'off_peak' in fares or 'total_cost' in fares:
                print("\nSUCCESS: Fare data extracted!")
            else:
                print("\nWARNING: No fare data found (check API response or time/date).")
        else:
            print("\nERROR: No journey found.")
            
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    main()
