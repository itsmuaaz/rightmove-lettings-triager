# Research: Overpass QL for Amenity Search

## Objective
Define the Overpass QL queries to fetch nearby amenities for the following categories:
1.  Supermarkets
2.  Gyms/Fitness Centers
3.  Parks/Green Spaces
4.  Healthcare Facilities

## Query Structure
We will use the `[out:json]` format and `around:radius` filter.
To simplify processing of ways and relations (which don't have a single lat/lon), we will use `out center;` which provides a center coordinate for all element types.

### Base Query Template
```
[out:json][timeout:25];
(
  node[{key}={value}](around:{radius},{lat},{lon});
  way[{key}={value}](around:{radius},{lat},{lon});
  relation[{key}={value}](around:{radius},{lat},{lon});
);
out center;
```

## Category Definitions

### 1. Supermarkets
- **Key:** `shop`
- **Value:** `supermarket`
- **Tags:** `node["shop"="supermarket"]`, `way["shop"="supermarket"]`
- **Note:** Some smaller stores might be `convenience` but spec asks for Supermarkets.

### 2. Gyms/Fitness Centers
- **Key:** `leisure`
- **Value:** `fitness_centre`
- **Tags:** `node["leisure"="fitness_centre"]`, `way["leisure"="fitness_centre"]`
- **Alternative:** `sport=fitness` is sometimes used but `leisure=fitness_centre` is the standard OSM tag for a gym. `leisure=sports_centre` is also relevant but might be a large complex. We will stick to `fitness_centre` and `sports_centre`.

### 3. Parks/Green Spaces
- **Key:** `leisure`
- **Value:** `park`
- **Tags:** `way["leisure"="park"]`, `relation["leisure"="park"]` (Parks are rarely single nodes)
- **Additional:** `landuse=recreation_ground`? `leisure=garden`?
- **Decision:** Focus on `leisure=park` and `leisure=garden`.

### 4. Healthcare
- **Key:** `amenity`
- **Values:** `hospital`, `doctors`
- **Tags:** `node["amenity"="hospital"]`, `way["amenity"="hospital"]`, `node["amenity"="doctors"]`

## Python Client Implementation Strategy
- Use `requests` library.
- Endpoint: `https://overpass-api.de/api/interpreter`
- Input: `data={query}`
- Response: JSON with `elements` list.
- Processing: Calculate distance from property to each element's `lat`/`lon` (or `center.lat`/`center.lon`).
