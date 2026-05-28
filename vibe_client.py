import json
import subprocess
import os
import sys
import time
from typing import Dict, List, Any

class VibeClient:
    """Client for fetching and caching 'vibe' data for London postcode districts using Gemini."""

    def __init__(self, cache_file: str = ".vibe_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        """Loads the cache from disk."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_cache(self):
        """Saves the cache to disk."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except IOError:
            pass

    def get_vibes(self, districts: List[str]) -> Dict[str, Any]:
        """Fetches vibe data for a list of postcode districts.
        
        Checks cache first, then batches remaining queries to Gemini.
        """
        results = {}
        missing = []

        # Check cache
        for district in districts:
            if district in self.cache:
                results[district] = self.cache[district]
            else:
                missing.append(district)

        # Log cache status transparently to avoid user confusion
        hits = len(districts) - len(missing)
        if hits > 0:
            sys.stderr.write(f"Vibe Cache: Loaded {hits}/{len(districts)} locations from '.vibe_cache.json' (0s delay).\n")

        if not missing:
            return results

        sys.stderr.write(f"Vibe Cache Miss: Fetching remaining {len(missing)} uncached locations from Gemini...\n")
        # Fetch missing in batches (simple implementation: one batch for now)
        fetched_data = self._fetch_from_gemini(missing)
        
        # Update cache and results
        for district, data in fetched_data.items():
            self.cache[district] = data
            results[district] = data
        
        self._save_cache()
        
        return results

    def _generate_prompt(self, locations: List[str]) -> str:
        return f"""
You are a London property market expert.
Analyze the 'vibe' of the following London locations (postcode districts or full addresses): {locations}.

Evaluate each location based on:
- Safety & Crime
- Fun & Nightlife
- Amenities (Supermarkets, Gyms, Cafes)
- Cleanliness & Street Appeal
- Quality of Life
- Access to Greenery (Parks, Commons)
- General Reputation & Prestige

For each location, provide a JSON object with:
1. "score": An aggregate integer (1-10) reflecting all the above factors.
   IMPORTANT: Avoid grade inflation. Use the full 1-10 range:
   - 1-3: Poor (High crime, dirty, no amenities)
   - 4-6: Average (Standard, functional, some issues)
   - 7-8: Good (Desirable, safe, good amenities)
   - 9-10: Excellent (Prestigious, beautiful, perfect location)
2. "summary": A concise 3-5 word description highlighting the dominant traits.
3. "safety": One of ["High", "Medium", "Low"].
4. "keywords": A list of 3 strings (e.g., ["Leafy", "Quiet", "Riverside"]).

Use a consistent scoring rubric across similar London areas.
Return ONLY a valid JSON object mapping the input location string exactly to the data. 
Do not include any markdown formatting (like ```json ... ```).

Example: 
{{
  "SW14": {{
    "score": 8, 
    "summary": "Leafy, safe, riverside village",
    "safety": "High",
    "keywords": ["Leafy", "Riverside", "Quiet"]
  }},
  "123 Example Street, London": {{
    "score": 6,
    "summary": "Busy, central, urban",
    "safety": "Medium",
    "keywords": ["Urban", "Busy", "Central"]
  }}
}}
"""

    def _fetch_from_gemini(self, locations: List[str]) -> Dict[str, Any]:
        """Calls Gemini CLI to analyze the given locations (postcodes or addresses), with retries."""
        if not locations:
            return {}

        prompt = self._generate_prompt(locations)
        max_retries = 3
        backoff_factor = 1

        for attempt in range(max_retries + 1):
            try:
                result = subprocess.run(
                    ["gemini", prompt],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                raw_output = result.stdout.strip()
                
                # Cleanup Markdown code blocks
                if raw_output.startswith("```json"):
                    raw_output = raw_output[7:]
                elif raw_output.startswith("```"):
                    raw_output = raw_output[3:]
                
                if raw_output.endswith("```"):
                    raw_output = raw_output[:-3]
                    
                return json.loads(raw_output.strip())
            
            except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError) as e:
                if attempt < max_retries:
                    sleep_time = backoff_factor * (2 ** attempt)
                    # print(f"Gemini call failed: {e}. Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                else:
                    # Log final failure
                    # print(f"Gemini call failed after {max_retries} retries: {e}")
                    return {}
        return {}
