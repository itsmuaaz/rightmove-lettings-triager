import time
import os
from unittest.mock import patch, MagicMock
from tfl_client import TflClient
import shutil

def verify_caching():
    # Setup
    test_dir = ".tfl_cache_verify"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    client = TflClient()
    client.cache_dir = test_dir
    
    # Mock API response
    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.read.return_value = b'{"journeys": [{"duration": 15}]}'
    mock_resp.__enter__.return_value = mock_resp
    
    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
        print("Run 1: Fetching (Should call API)")
        d1 = client.get_commute_time((51.5, 0.1), (51.6, 0.2))
        print(f"Result: {d1}")
        
        # Verify file exists
        files = os.listdir(test_dir)
        if files:
            print(f"Cache file created: {files[0]}")
        else:
            print("ERROR: No cache file created!")
            return

        print("\nRun 2: Fetching same route (Should use cache)")
        d2 = client.get_commute_time((51.5, 0.1), (51.6, 0.2))
        print(f"Result: {d2}")
        
        if mock_urlopen.call_count == 1:
            print("SUCCESS: API was called only once!")
        else:
            print(f"FAILURE: API was called {mock_urlopen.call_count} times.")

    # Cleanup
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    verify_caching()
