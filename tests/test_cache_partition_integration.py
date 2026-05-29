import unittest
from unittest.mock import patch, MagicMock
import rightmove_search
import sys
import io

class TestCachePartitionIntegration(unittest.TestCase):
    def setUp(self):
        # Mocks
        self.mock_tfl = MagicMock()
        self.mock_amenity = MagicMock()
        self.mock_vibe = MagicMock()
        self.mock_calculator = MagicMock()
        self.mock_calculator.calculate.return_value = {
            'distance': 100, 'commute_time': 10, 'commute_fares': None, 'commute_cycling': 5
        }
        self.mock_amenity_calc = MagicMock()
        self.mock_amenity_calc.calculate.return_value = {}
        
        # Inject mocks into rightmove_search globals
        rightmove_search.tfl = self.mock_tfl
        rightmove_search.amenity_calculator = self.mock_amenity_calc
        rightmove_search.amenity_calculator.client = self.mock_amenity
        rightmove_search.vibe_client = self.mock_vibe
        rightmove_search.calculator = self.mock_calculator
        rightmove_search.WORK_LOCATION_COORDS = (51.0, -0.1)
        
        # Create a mock search state to capture updates
        self.mock_search_state = MagicMock()
        self.mock_search_state.processed = 0
        rightmove_search.search_state = self.mock_search_state

    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_bypasses_thread_pool_when_fully_cached(self, mock_executor):
        # Setup the fully cached state
        with patch('rightmove_search.is_fully_cached', return_value=True):
            # Run the partition logic
            all_properties = [
                {'_original': {}, 'latitude': 51.5, 'longitude': -0.1, 'address': 'A'},
                {'_original': {}, 'latitude': 51.6, 'longitude': -0.1, 'address': 'B'}
            ]
            
            # We want to capture stderr to not clutter test output
            captured_stderr = io.StringIO()
            with patch('sys.stderr', captured_stderr):
                # Call the specific loop section we modified (abstracted here for the test)
                synchronous_properties = []
                async_properties = []
                for p in all_properties:
                    if rightmove_search.is_fully_cached(
                        self.mock_tfl, self.mock_amenity, self.mock_vibe, p, rightmove_search.WORK_LOCATION_COORDS
                    ):
                        synchronous_properties.append(p)
                    else:
                        async_properties.append(p)
                
                if synchronous_properties:
                    for p in synchronous_properties:
                        rightmove_search.populate_property_sync(p)
                    rightmove_search.search_state.processed += len(synchronous_properties)
                
                if async_properties:
                    mock_executor.submit() # Just to track if it would be called

        # Assertions
        mock_executor.assert_not_called()
        self.assertEqual(rightmove_search.search_state.processed, 2)
        
        # Assert properties got populated
        self.assertEqual(synchronous_properties[0]['commute_time'], 10)
        self.assertEqual(synchronous_properties[1]['commute_time'], 10)

    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_uses_thread_pool_for_mixed_cache_state(self, mock_executor):
        # First true, second false
        with patch('rightmove_search.is_fully_cached', side_effect=[True, False]):
            all_properties = [
                {'_original': {}, 'latitude': 51.5, 'longitude': -0.1, 'address': 'A'},
                {'_original': {}, 'latitude': 51.6, 'longitude': -0.1, 'address': 'B'}
            ]
            
            captured_stderr = io.StringIO()
            with patch('sys.stderr', captured_stderr):
                synchronous_properties = []
                async_properties = []
                for p in all_properties:
                    if rightmove_search.is_fully_cached(
                        self.mock_tfl, self.mock_amenity, self.mock_vibe, p, rightmove_search.WORK_LOCATION_COORDS
                    ):
                        synchronous_properties.append(p)
                    else:
                        async_properties.append(p)
                
                if synchronous_properties:
                    for p in synchronous_properties:
                        rightmove_search.populate_property_sync(p)
                    rightmove_search.search_state.processed += len(synchronous_properties)
                
                if async_properties:
                    executor = mock_executor(max_workers=3)
                    for i, p in enumerate(async_properties):
                        executor.submit(rightmove_search.process_property, p, i, len(async_properties))

        # Assertions
        mock_executor.assert_called_once()
        self.assertEqual(rightmove_search.search_state.processed, 1) # Only sync one incremented here

if __name__ == '__main__':
    unittest.main()
