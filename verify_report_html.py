from reporter import Reporter
import re

def main():
    reporter = Reporter()
    
    prop = {
        'id': 'test-prop-1',
        'address': '10 Downing Street',
        'commute_time': 45,
        'commute_fares': {'peak': 350, 'off_peak': 280},
        'location': {'latitude': 51.5, 'longitude': -0.1},
        'price': '£1,000 pcm',
        'status': 'new'
    }
    
    print("Generating report...")
    html = reporter.generate_report([prop])
    
    # Check for fare string in HTML
    expected = "(£3.50 / £2.80)"
    if expected in html:
        print(f"SUCCESS: Found '{expected}' in generated HTML.")
    else:
        print(f"ERROR: Could not find '{expected}' in generated HTML.")
        print("Snippet around commute time:")
        match = re.search(r'45 min(.*?)</div', html, re.DOTALL)
        if match:
            print(match.group(1))
        else:
            print("Could not find commute time in HTML.")

if __name__ == "__main__":
    main()
