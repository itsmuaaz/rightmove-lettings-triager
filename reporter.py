from utils import format_date, generate_google_maps_url, generate_tfl_url
import markdown
from string import Template

class Reporter:
    """Generates Markdown and HTML reports for property search results."""

    def __init__(self):
        self.headers = ["Image", "Price", "Commute", "Nearby Amenities", "Distance", "Notes", "Details", "Address", "Added On", "Link"]

    def _get_commute_class(self, minutes):
        """Returns the CSS class for the commute badge."""
        if minutes is None:
            return "badge-grey"
        try:
            mins = int(minutes)
            if mins < 20:
                return "badge-green"
            elif mins <= 40:
                return "badge-amber"
            else:
                return "badge-red"
        except (ValueError, TypeError):
            return "badge-grey"

    def _sanitize(self, text):
        """Removes pipes and newlines to prevent breaking Markdown tables."""
        if not isinstance(text, str):
            return text
        return text.replace("|", " ").replace("\n", " ").replace("\r", " ").strip()

    def _generate_commute_cell(self, p, for_html=False):
        """Generates the commute cell content."""
        commute_mins = p.get("commute_time")
        cycling_mins = p.get("commute_cycling")
        
        # Helper to format a single badge
        def format_badge(mins, icon):
            cls = self._get_commute_class(mins)
            txt = f"{mins} mins {icon}" if mins is not None else "N/A"
            return f'<span class="{cls}">{txt}</span>'

        items = []
        if commute_mins is not None or cycling_mins is None:
             items.append(format_badge(commute_mins, "🚆"))
        
        if cycling_mins is not None:
             items.append(format_badge(cycling_mins, "🚲"))
             
        if not items:
            return '<span class="badge-grey">N/A</span>'

        # Generate Links
        origin_address = p.get('address', '')
        origin_coords = None
        if p.get('latitude') and p.get('longitude'):
            origin_coords = (p.get('latitude'), p.get('longitude'))
            
        gmaps_link = generate_google_maps_url(origin_address)
        tfl_link = generate_tfl_url(origin_address, origin_coords)

        if for_html:
            badges_html = "".join(items)
            links_html = f'<div class="commute-links"><a href="{gmaps_link}" target="_blank">[GMaps]</a> <a href="{tfl_link}" target="_blank">[TfL]</a></div>'
            return f'<div class="commute-stack">{badges_html}{links_html}</div>'
        else:
            badges_md = " / ".join(items)
            links_md = f"[GMaps]({gmaps_link}) [TfL]({tfl_link})"
            return f"{badges_md} <br> {links_md}"

    def _generate_amenity_cell(self, p, for_html=False):
        """Generates the nearby amenities cell content."""
        amenities = p.get('nearby_amenities')
        
        if amenities is None:
            return '<span class="badge-grey">Data Error</span>' if for_html else "⚠ Data Error"

        cat_labels = {
            'supermarket': '🛒',
            'gym': '💪',
            'park': '🌳',
            'healthcare': '🏥'
        }
        
        parts = []
        for key, label in cat_labels.items():
            item = amenities.get(key) if amenities else None
            if item:
                name = item.get('name', 'Unknown')
                dist = int(item.get('distance', 0))
                mins = max(1, round(dist / 80)) # 80m/min walking speed
                parts.append(f"{label} {name} (~{mins} mins)")
            else:
                parts.append(f"{label} None nearby")
                
        if for_html:
            items_html = [f'<div>{part}</div>' for part in parts]
            return f'<div style="font-size: 0.8em; line-height: 1.2;">{"".join(items_html)}</div>'
        else:
            return " <br> ".join(parts)

    def _generate_notes_cell(self, p, for_html=False):
        """Generates the editable notes cell."""
        note_content = p.get('note') or ''
        prop_id = p.get('id', '')
        
        if for_html and prop_id:
            # Escape quotes for safety
            escaped_content = note_content.replace('"', '&quot;')
            return f'''<textarea class="note-input" placeholder="Start typing..." 
                       onblur="saveNote('{prop_id}', this.value)">{note_content}</textarea>'''
        else:
            return note_content if note_content else "N/A"

    def _generate_row(self, p, for_html=False):
        """Generates a Markdown table row for a property."""
        image_html = f'<img src="{p.get("image_url")}" class="prop-img" alt="Property">' if p.get("image_url") else "N/A"
        
        commute_html = self._generate_commute_cell(p, for_html)
        amenity_html = self._generate_amenity_cell(p, for_html)
        notes_html = self._generate_notes_cell(p, for_html)
        
        dist_val = p.get("distance")
        dist_str = f"{dist_val:.2f} mi" if dist_val else "N/A"
        
        details = self._sanitize(f"{p.get('bedrooms', 0)} bed {p.get('type', 'Property')}")
        address = self._sanitize(p.get('address'))
        added_on = format_date(p.get("published_on"))
        
        link = f"https://www.rightmove.co.uk{p.get('url', '')}"
        link_html = f'[View]({link})'

        return f"| {image_html} | **{p.get('price')}** | {commute_html} | {amenity_html} | {dist_str} | {notes_html} | {details} | {address} | {added_on} | {link_html} |"

    def generate_markdown(self, properties, for_html=False):
        """Generates the full Markdown report."""
        header_row = "| " + " | ".join(self.headers) + " |\n"
        separator_row = "| " + " | ".join(["---"] * len(self.headers)) + " |\n"
        
        md = header_row + separator_row
        
        for p in properties:
            md += self._generate_row(p, for_html) + "\n"
            
        return md

    def convert_to_html(self, md_content):
        """Converts Markdown content to a styled HTML report."""
        html_table = markdown.markdown(md_content, extensions=['tables'])
        template = Template(self.get_html_template())
        return template.substitute(content=html_table)

    def get_html_template(self):
        """Returns the HTML boilerplate with embedded CSS and JS."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Property Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 20px; color: #333; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: top; }
        th { background-color: #f2f2f2; font-weight: 600; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        
        .prop-img { max-width: 150px; height: auto; border-radius: 4px; object-fit: cover; }
        
        /* Commute Badges */
        span[class^="badge-"] { padding: 4px 8px; border-radius: 4px; font-weight: 500; font-size: 0.9em; display: inline-block; }
        .badge-green { background-color: #d4edda; color: #155724; }
        .badge-amber { background-color: #fff3cd; color: #856404; }
        .badge-red { background-color: #f8d7da; color: #721c24; }
        .badge-grey { background-color: #e2e3e5; color: #383d41; }

        .commute-stack { display: flex; flex-direction: column; gap: 4px; }
        .commute-links { margin-top: 4px; font-size: 0.85em; }
        
        /* Notes */
        .note-input { width: 100%; height: 80px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; resize: vertical; font-family: inherit; }
        .note-input:focus { border-color: #007bff; outline: none; }
        
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
    <script>
        function saveNote(propertyId, text) {
            fetch('/api/notes', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: propertyId, note: text})
            }).then(response => {
                if (response.ok) {
                    console.log('Note saved for ' + propertyId);
                } else {
                    console.error('Failed to save note for ' + propertyId);
                    alert('Failed to save note. Check connection.');
                }
            }).catch(err => {
                console.error('Error saving note:', err);
            });
        }
    </script>
</head>
<body>
    <h1>Property Search Results</h1>
    <p>Generated report. Use the text areas to save notes.</p>
    <div id="content">
        $content
    </div>
</body>
</html>
"""
