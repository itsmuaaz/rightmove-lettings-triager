from reporter import Reporter
import os

def verify_dashboard_rendering():
    # Mock property data with agency info
    properties = [
        {
            'id': '1',
            'address': '123 High St, London',
            'price': '£1,500 pcm',
            'type': 'Flat',
            'agency_name': 'OpenRent, London',
            'agency_phone': '020 1234 5678',
            'url': 'https://rightmove.co.uk/prop/1',
            'images': [],
            'status': 'new',
            'commute_time': 30,
            'vibe_score': 8.5
        },
        {
            'id': '2',
            'address': '456 Low St, London',
            'price': '£1,200 pcm',
            'type': 'Studio',
            'agency_name': 'Foxtons',
            'agency_phone': '', # Missing phone
            'url': 'https://rightmove.co.uk/prop/2',
            'images': [],
            'status': 'viewed',
            'commute_time': 45,
            'vibe_score': 6.0
        },
        {
            'id': '3',
            'address': '789 No Agency St, London',
            'price': '£1,000 pcm',
            'type': 'Room',
            'agency_name': '', # Missing name
            'agency_phone': '07700 900000',
            'url': 'https://rightmove.co.uk/prop/3',
            'images': [],
            'status': 'shortlisted',
            'commute_time': 15,
            'vibe_score': 9.0
        }
    ]

    reporter = Reporter()
    html = reporter.generate_report(properties, processed_count=3, total_count=3)

    output_file = 'verify_dashboard.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated {output_file}. Please open it in a browser to verify rendering.")
    
    # Simple assertion: check if agency info is in the HTML
    if 'OpenRent, London' in html and '020 1234 5678' in html:
        print("SUCCESS: Agency info found in HTML.")
    else:
        print("FAILURE: Agency info NOT found in HTML.")

if __name__ == "__main__":
    verify_dashboard_rendering()
