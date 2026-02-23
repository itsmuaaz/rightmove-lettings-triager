from tfl_client import TflClient
import time
import shutil
import os
import threading

def verify_rate_limiting():
    # Setup
    test_dir = ".tfl_cache_verify_rate"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Use interval of 0.5s for faster visual verification
    # Default is 1.5s, which is slower.
    interval = 0.5
    client = TflClient(min_interval=interval)
    client.cache_dir = test_dir
    
    print(f"Verifying Rate Limiting (Interval: {interval}s)...")
    
    start_time = time.time()
    
    # Simulate 5 rapid requests
    # Since we don't want to hit real API 5 times (might get banned or fail auth),
    # we rely on the fact that _wait_for_slot happens BEFORE the request.
    # We can use a trick: cache hits bypass wait. Cache misses hit wait.
    # But checking 'wait' directly requires mocking or checking timing.
    
    # Let's just check timing of "attempts".
    # We will call _wait_for_slot directly to verify it works, 
    # OR we can try to hit a dummy endpoint if possible? No.
    
    # We will use the client's internal mechanism.
    # Since _wait_for_slot is public-ish (protected), we can call it.
    
    print("Simulating 4 requests...")
    for i in range(4):
        loop_start = time.time()
        client._wait_for_slot()
        print(f"Request {i+1} slot acquired at {time.time() - start_time:.2f}s")
        # Simulating request time
        time.sleep(0.01) 
        
    total_time = time.time() - start_time
    # 4 requests:
    # 1st: immediate (0.0s)
    # 2nd: wait 0.5s -> 0.5s
    # 3rd: wait 0.5s -> 1.0s
    # 4th: wait 0.5s -> 1.5s
    # Total should be around 1.5s
    
    print(f"Total time for 4 requests: {total_time:.2f}s")
    if total_time >= 1.4:
        print("SUCCESS: Rate limiting is active.")
    else:
        print("FAILURE: Rate limiting seems too fast.")

    # Cleanup
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    verify_rate_limiting()
