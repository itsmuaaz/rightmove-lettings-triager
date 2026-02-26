import re

with open('results.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract properties blocks
blocks = content.split('<tr id="property-')[1:]

properties = []
for block in blocks:
    prop_id_match = re.search(r'^([^"]+)"', block)
    if not prop_id_match:
        continue
    prop_id = prop_id_match.group(1)
    
    # Address
    address_match = re.search(r'<a href="[^"]+" target="_blank" class="hover:underline text-blue-600 visited:text-purple-600"[^>]*>\s*(.*?)\s*</a>', block, re.DOTALL)
    address = address_match.group(1).strip() if address_match else "Unknown"
    
    # URL
    url_match = re.search(r'<a href="([^"]+)" target="_blank" class="hover:underline text-blue-600 visited:text-purple-600"', block)
    url = url_match.group(1) if url_match else ""
    
    # Price
    price_match = re.search(r'<div class="text-sm font-bold text-gray-900">\s*(.*?)\s*</div>', block)
    price = price_match.group(1).strip() if price_match else "Unknown"
    
    # Vibe score
    vibe_match = re.search(r'<span class="text-xl font-bold [^"]+ mt-0\.5">\s*(.*?)\s*</span>', block)
    vibe = vibe_match.group(1).strip() if vibe_match else "N/A"
    
    # Commute
    commute_match = re.search(r'<span class="font-semibold">\s*(.*?)\s*min</span>', block)
    commute = commute_match.group(1).strip() if commute_match else "N/A"
    
    # Cycling
    cycling_match = re.search(r'<div class="flex items-center text-sm [^"]*">\s*<span class="mr-1">🚲</span>\s*<span>\s*(.*?)\s*min</span>', block, re.DOTALL)
    cycling = cycling_match.group(1).strip() if cycling_match else "N/A"

    # Status
    status = "normal"
    if "bg-yellow-100" in block:
        status = "shortlisted"
    elif "bg-gray-200 opacity-50" in block:
        status = "dismissed"

    properties.append({
        "id": prop_id,
        "address": address,
        "url": url,
        "price": price,
        "vibe": vibe,
        "commute": commute,
        "cycling": cycling,
        "status": status
    })

good_properties = []
for p in properties:
    if p['status'] == 'dismissed':
        continue
    
    vibe_score = 0
    try:
        if p['vibe'] not in ('N/A', 'None'):
            vibe_score = float(p['vibe'])
    except Exception:
        pass
        
    commute_time = 999
    try:
        if p['commute'] not in ('N/A', 'Loading...'):
            commute_time = int(p['commute'])
    except Exception:
        pass
        
    p['vibe_score'] = vibe_score
    p['commute_time'] = commute_time
    
    if vibe_score >= 6 and commute_time <= 45:
        good_properties.append(p)

good_properties.sort(key=lambda x: (-x['vibe_score'], x['commute_time']))

print(f"Total parsed: {len(properties)}")
shortlisted = [p for p in properties if p['status'] == 'shortlisted']
print(f"Total shortlisted: {len(shortlisted)}")
print(f"Total good properties (vibe >=6, commute <=45): {len(good_properties)}")

print("\n--- TOP 15 PROPERTIES ---")
for i, p in enumerate(good_properties[:15]):
    print(f"{i+1}. {p['address']}")
    print(f"   Price: {p['price']} | Vibe: {p['vibe']} | Commute: {p['commute']} min | Cycling: {p['cycling']} min")
    print(f"   URL: {p['url']}")
    print(f"   Status: {p['status']}\n")
