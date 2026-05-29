import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import shutil

from rightmove_search import is_tfl_cached, is_osm_cached, is_vibe_cached, is_fully_cached

class TestCachePartitioning(unittest.TestCase):
    def setUp(self):
        self.tfl_client = MagicMock()
        self.amenity_client = MagicMock()
        self.vibe_client = MagicMock()
        self.work_coords = (51.0, -0.1)
        self.prop = {'latitude': 51.5, 'longitude': -0.2, 'displayAddress': 'Test St'}

    def test_is_tfl_cached(self):
        self.tfl_client.is_cached.side_effect = [True, True]
        self.assertTrue(is_tfl_cached(self.tfl_client, (51.5, -0.2), self.work_coords))
        
        self.tfl_client.is_cached.side_effect = [True, False]
        self.assertFalse(is_tfl_cached(self.tfl_client, (51.5, -0.2), self.work_coords))
        
        self.tfl_client.is_cached.side_effect = [False, True]
        self.assertFalse(is_tfl_cached(self.tfl_client, (51.5, -0.2), self.work_coords))

    def test_is_osm_cached(self):
        self.amenity_client.is_cached.return_value = True
        self.assertTrue(is_osm_cached(self.amenity_client, 51.5, -0.2))
        
        self.amenity_client.is_cached.return_value = False
        self.assertFalse(is_osm_cached(self.amenity_client, 51.5, -0.2))

    def test_is_vibe_cached(self):
        self.vibe_client.cache = {'SW1': {'cached_at': '2026-05-28T12:00:00'}}
        self.assertTrue(is_vibe_cached(self.vibe_client, 'SW1'))
        
        self.vibe_client.cache = {'SW1': {}} # No timestamp
        self.assertFalse(is_vibe_cached(self.vibe_client, 'SW1'))
        
        self.vibe_client.cache = {} # Missing entirely
        self.assertFalse(is_vibe_cached(self.vibe_client, 'SW1'))

    @patch('rightmove_search.extract_location_for_vibe', return_value='SW1')
    def test_is_fully_cached(self, mock_extract):
        # All hit
        self.tfl_client.is_cached.return_value = True
        self.amenity_client.is_cached.return_value = True
        self.vibe_client.cache = {'SW1': {'cached_at': '2026-05-28T12:00:00'}}
        
        self.assertTrue(is_fully_cached(self.tfl_client, self.amenity_client, self.vibe_client, self.prop, self.work_coords))
        
        # Miss TfL
        self.tfl_client.is_cached.return_value = False
        self.assertFalse(is_fully_cached(self.tfl_client, self.amenity_client, self.vibe_client, self.prop, self.work_coords))
        
        # Miss Amenity
        self.tfl_client.is_cached.return_value = True
        self.amenity_client.is_cached.return_value = False
        self.assertFalse(is_fully_cached(self.tfl_client, self.amenity_client, self.vibe_client, self.prop, self.work_coords))

        # Miss Vibe
        self.amenity_client.is_cached.return_value = True
        self.vibe_client.cache = {}
        self.assertFalse(is_fully_cached(self.tfl_client, self.amenity_client, self.vibe_client, self.prop, self.work_coords))

    def test_is_fully_cached_missing_coords(self):
        self.assertFalse(is_fully_cached(self.tfl_client, self.amenity_client, self.vibe_client, {}, self.work_coords))

if __name__ == '__main__':
    unittest.main()
