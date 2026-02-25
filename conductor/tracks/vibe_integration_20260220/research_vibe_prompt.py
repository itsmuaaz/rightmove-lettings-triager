import subprocess
import json
import sys

def test_prompt(districts):
    prompt = f"""
You are a London property market expert.
Analyze the 'vibe' of the following London postcode districts: {districts}.

For each district, provide a JSON object with:
1. "score": An integer (1-10) reflecting safety, prestige, and amenities (10 = Excellent).
2. "summary": A concise 3-5 word description (e.g., "Affluent, green, family-friendly").
3. "safety": One of ["High", "Medium", "Low"].
4. "keywords": A list of 3 strings (e.g., ["Leafy", "Quiet", "Riverside"]).

Return ONLY a valid JSON object mapping the district to the data. 
Do not include any markdown formatting (like ```json ... ```).
Example: 
{{
  "SW14": {{
    "score": 8, 
    "summary": "Leafy, safe, riverside village",
    "safety": "High",
    "keywords": ["Leafy", "Riverside", "Quiet"]
  }}
}}
"""
    print(f"--- Testing Prompt with districts: {districts} ---")
    try:
        # Using the CLI via subprocess
        # Note: Depending on the environment, 'gemini' might be an alias or function.
        # If 'gemini' command is not found, we might need to know how the user runs it.
        # Assuming 'gemini' is in the PATH as per instructions.
        result = subprocess.run(
            ["gemini", prompt], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print("Raw Output:")
        print(result.stdout)
        
        try:
            # excessive cleanup just in case
            cleaned = result.stdout.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            data = json.loads(cleaned)
            print("\nParsed JSON:")
            print(json.dumps(data, indent=2))
            return True
        except json.JSONDecodeError as e:
            print(f"\nJSON Parse Error: {e}")
            return False

    except FileNotFoundError:
        print("Error: 'gemini' command not found.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error calling gemini: {e}")
        print(e.stderr)
        return False

if __name__ == "__main__":
    districts = ["SW14", "E1", "N1C", "CR0"]
    test_prompt(districts)
