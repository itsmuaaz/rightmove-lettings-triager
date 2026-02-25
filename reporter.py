from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils import format_date, generate_google_maps_url, generate_tfl_url
from datetime import datetime
import os

class Reporter:
    """Generates HTML reports for property search results using Jinja2."""

    def __init__(self, template_dir="templates"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def _get_commute_class(self, minutes):
        """Returns the Tailwind color class for the commute badge."""
        if minutes is None:
            return "text-gray-500"
        try:
            mins = int(minutes)
            if mins < 20:
                return "text-green-600"
            elif mins <= 40:
                return "text-amber-600"
            else:
                return "text-red-600"
        except (ValueError, TypeError):
            return "text-gray-500"

    def _process_amenities(self, amenities_dict):
        """Transforms amenities dict into a list for the template."""
        if not amenities_dict:
            return []
        
        processed = []
        cat_labels = {
            'supermarket': ('🛒', 'bg-blue-500'),
            'gym': ('💪', 'bg-red-500'),
            'park': ('🌳', 'bg-green-500'),
            'healthcare': ('🏥', 'bg-purple-500')
        }

        for key, (icon, color_class) in cat_labels.items():
            item = amenities_dict.get(key)
            if item:
                name = item.get('name', 'Unknown')
                dist = int(item.get('distance', 0))
                mins = max(1, round(dist / 80))
                processed.append({
                    'name': f"{icon} {name}",
                    'distance': f"~{mins} mins",
                    'color_class': color_class
                })
            else:
                # Option to show missing amenities or just skip
                # Template seems to iterate over existing ones
                pass
        return processed

    def _enrich_property(self, p):
        """Enriches a property dict with display-ready fields."""
        # Clone to avoid mutating original if needed, but here we modify for display
        
        # Commute
        commute_mins = p.get("commute_time")
        p['commute_color_class'] = self._get_commute_class(commute_mins)
        p['commute_time'] = commute_mins if commute_mins is not None else "N/A"
        
        cycling_mins = p.get("commute_cycling")
        p['cycling_time'] = cycling_mins if cycling_mins is not None else "N/A"

        # Links
        origin_address = p.get('address', '')
        origin_coords = None
        if p.get('latitude') and p.get('longitude'):
            origin_coords = (p.get('latitude'), p.get('longitude'))
        
        p['google_maps_link'] = generate_google_maps_url(origin_address)
        p['tfl_link'] = generate_tfl_url(origin_address, origin_coords)
        
        # Amenities
        p['amenities'] = self._process_amenities(p.get('nearby_amenities'))

        # Dates/Formatting
        p['added_on'] = format_date(p.get("published_on"))
        
        # Prices
        # Assuming price is already formatted or we might need to split it
        # p['price'] is usually string like "£2,000 pcm"
        # We can keep it or parse it if template needs separate pcm/pw
        # Template uses price_pcm and price_pw if available.
        if 'price' in p and 'price_pcm' not in p:
             p['price_pcm'] = p['price'] # Fallback
             p['price_pw'] = "N/A" # Fallback

        # Status
        history = p.get('history_status', {}) or {}
        p['status'] = history.get('status', 'new')
        p['is_new'] = (p['status'] == 'new')
        
        # Ensure ID exists
        if 'id' not in p and 'url' in p:
             # Fallback ID generation if missing (should exist from search)
             p['id'] = str(hash(p['url']))

        # Notes
        p['notes'] = p.get('note', '')

        # Images
        if 'image_url' in p and 'images' not in p:
            p['images'] = [p['image_url']]
        
        return p

    def generate_report(self, properties, shortlist=None, filters=None):
        """Generates the HTML report."""
        template = self.env.get_template("report.html")
        
        enriched_properties = [self._enrich_property(p) for p in properties]
        
        enriched_shortlist = []
        if shortlist:
             enriched_shortlist = [self._enrich_property(p) for p in shortlist]
        elif shortlist is None:
             # Auto-derive shortlist from properties if not provided separately
             enriched_shortlist = [p for p in enriched_properties if p.get('status') == 'shortlisted']

        return template.render(
            properties=enriched_properties,
            shortlist=enriched_shortlist,
            filters=filters,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
