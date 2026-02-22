import unittest
import time
import threading
from tfl_client import TflClient

class TestTflClientRateLimiting(unittest.TestCase):
    def setUp(self):
        self.client = TflClient()
        # Override rate limit for faster testing
        # We want to test the mechanism, not wait for 1.5s real time every time
        self.client.min_interval = 0.1 

    def test_wait_for_slot_enforces_interval(self):
        """Test that _wait_for_slot pauses execution to respect the interval."""
        start_time = time.time()
        
        # First call should be immediate
        self.client._wait_for_slot()
        t1 = time.time()
        
        # Second call should wait
        self.client._wait_for_slot()
        t2 = time.time()
        
        # Verify delay
        # The first call updates last_request_time.
        # The second call must happen at least min_interval seconds after the first.
        self.assertGreaterEqual(t2 - t1, 0.09) # Allow small margin for error

    def test_wait_for_slot_thread_safety(self):
        """Test that rate limiting works across multiple threads."""
        self.client.min_interval = 0.2
        
        start_time = time.time()
        threads = []
        
        def worker():
            self.client._wait_for_slot()
            
        # Launch 3 threads
        for _ in range(3):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Expected:
        # T1: 0.0s (immediate)
        # T2: 0.2s (waits for T1)
        # T3: 0.4s (waits for T2)
        # Total duration should be at least 0.4s (2 intervals)
        self.assertGreaterEqual(duration, 0.38)

if __name__ == '__main__':
    unittest.main()
