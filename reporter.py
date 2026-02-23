from utils import format_date, generate_google_maps_url, generate_tfl_url
import markdown
import html
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
            escaped_content = html.escape(note_content)
            return f'<textarea class="note-input" placeholder="Start typing..." onblur="saveNote(\'{prop_id}\', this.value)">{escaped_content}</textarea>'
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

    def _generate_html_row(self, p):
        """Generates an HTML table row for a property."""
        prop_id = p.get('id', '')
        history = p.get('history_status', {}) or {}
        status = history.get('status', 'new')
        
        row_class = f"prop-row status-{status}"
        
        # New Badge
        new_badge = '<span class="badge-new">NEW</span>' if status == 'new' else ''
        
        image_html = f'<div class="img-container">{new_badge}<img src="{p.get("image_url")}" class="prop-img" alt="Property"></div>' if p.get("image_url") else "N/A"
        
        commute_html = self._generate_commute_cell(p, for_html=True)
        amenity_html = self._generate_amenity_cell(p, for_html=True)
        notes_html = self._generate_notes_cell(p, for_html=True)
        
        dist_val = p.get("distance")
        dist_str = f"{dist_val:.2f} mi" if dist_val else "N/A"
        
        details = self._sanitize(f"{p.get('bedrooms', 0)} bed {p.get('type', 'Property')}")
        address = self._sanitize(p.get('address'))
        added_on = format_date(p.get("published_on"))
        
        link = f"https://www.rightmove.co.uk{p.get('url', '')}"
        
        # Actions
        view_btn = f'<a href="{link}" target="_blank" class="btn btn-view" onclick="markViewed(\'{prop_id}\', this)">View</a>'
        dismiss_btn = f'<button class="btn btn-dismiss" onclick="dismissProperty(\'{prop_id}\', this)">Dismiss</button>'
        undo_btn = f'<button class="btn btn-undo" onclick="undoDismiss(\'{prop_id}\', this)">Undo</button>'
        
        actions_html = f'<div class="action-stack">{view_btn}{dismiss_btn}{undo_btn}</div>'

        cells = [image_html, f"<strong>{p.get('price')}</strong>", commute_html, amenity_html, dist_str, notes_html, details, address, added_on, actions_html]
        row_content = "".join([f"<td>{c}</td>" for c in cells])
        return f'<tr class="{row_class}" id="row-{prop_id}">{row_content}</tr>'

    def generate_html_report(self, properties):
        """Generates the full HTML report directly."""
        header_row = "".join([f"<th>{h}</th>" for h in self.headers])
        thead = f"<thead><tr>{header_row}</tr></thead>"
        
        rows = "".join([self._generate_html_row(p) for p in properties])
        tbody = f"<tbody>{rows}</tbody>"
        
        table = f"<table>{thead}{tbody}</table>"
        template = Template(self.get_html_template())
        return template.substitute(content=table)

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
        .img-container { position: relative; display: inline-block; }
        
        /* Status Styles */
        tr.status-new { background-color: #e6fffa !important; border-left: 4px solid #38b2ac; }
        tr.status-shortlisted { background-color: #fffaf0 !important; border-left: 4px solid #ecc94b; opacity: 1 !important; }
        tr.status-viewed { opacity: 0.6; filter: grayscale(20%); }
        tr.status-dismissed { opacity: 0.3; filter: grayscale(100%); max-height: 50px; overflow: hidden; }
        /* Hide details when dismissed */
        tr.status-dismissed td { padding-top: 5px; padding-bottom: 5px; }
        tr.status-dismissed .prop-img, tr.status-dismissed .commute-stack, tr.status-dismissed .note-input { display: none; }
        
        /* Badges */
        .badge-new { position: absolute; top: -5px; right: -5px; background: #e53e3e; color: white; font-size: 0.7em; padding: 2px 6px; border-radius: 10px; font-weight: bold; box-shadow: 0 1px 3px rgba(0,0,0,0.2); z-index: 10; }
        
        span[class^="badge-"] { padding: 4px 8px; border-radius: 4px; font-weight: 500; font-size: 0.9em; display: inline-block; }
        .badge-green { background-color: #d4edda; color: #155724; }
        .badge-amber { background-color: #fff3cd; color: #856404; }
        .badge-red { background-color: #f8d7da; color: #721c24; }
        .badge-grey { background-color: #e2e3e5; color: #383d41; }

        .commute-stack { display: flex; flex-direction: column; gap: 4px; }
        .commute-links { margin-top: 4px; font-size: 0.85em; }
        
        /* Actions */
        .action-stack { display: flex; flex-direction: column; gap: 5px; }
        .btn { padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9em; text-align: center; text-decoration: none; color: white; display: inline-block; }
        .btn-view { background-color: #3182ce; }
        .btn-dismiss { background-color: #718096; }
        .btn-shortlist { background-color: #d69e2e; }
        .btn-undo { background-color: #38a169; display: none; }
        
        /* Show Undo only when dismissed */
        tr.status-dismissed .btn-dismiss { display: none; }
        tr.status-dismissed .btn-undo { display: inline-block; }
        tr.status-dismissed .btn-view, tr.status-dismissed .btn-shortlist { display: none; }

        /* Notes */
        .note-input { width: 100%; height: 80px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; resize: vertical; font-family: inherit; box-sizing: border-box; }
        .note-input:focus { border-color: #007bff; outline: none; }
        
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        
        #mark-all-btn { margin-bottom: 10px; padding: 10px 20px; font-size: 1em; background-color: #2b6cb0; color: white; border: none; border-radius: 4px; cursor: pointer; }
    </style>
    <script>
        async function apiCall(endpoint, data) {
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                return response.ok;
            } catch (err) {
                console.error('API Error:', err);
                return false;
            }
        }

        function saveNote(propertyId, text) {
            apiCall('/api/notes', {id: propertyId, note: text});
        }

        function markViewed(id, el) {
            // Optimistic update
            const row = document.getElementById('row-' + id);
            if (row) {
                row.classList.remove('status-new');
                // Only mark as viewed if not already shortlisted
                if (!row.classList.contains('status-shortlisted')) {
                    row.classList.add('status-viewed');
                }
                const badge = row.querySelector('.badge-new');
                if (badge) badge.remove();
            }
            apiCall('/api/history', {id: id, action: 'view'});
            // Allow link to open
            return true;
        }

        function markShortlisted(id, btn) {
            const row = document.getElementById('row-' + id);
            if (row) {
                row.classList.remove('status-new', 'status-viewed');
                row.classList.add('status-shortlisted');
                const badge = row.querySelector('.badge-new');
                if (badge) badge.remove();
            }
            apiCall('/api/history', {id: id, action: 'shortlist'});
        }

        function dismissProperty(id, btn) {
            const row = document.getElementById('row-' + id);
            if (row) {
                row.classList.remove('status-new', 'status-viewed', 'status-shortlisted');
                row.classList.add('status-dismissed');
            }
            apiCall('/api/history', {id: id, action: 'dismiss'});
        }

        function undoDismiss(id, btn) {
            const row = document.getElementById('row-' + id);
            if (row) {
                row.classList.remove('status-dismissed');
                // Could be either viewed or shortlisted. 
                // For simplicity, default back to viewed unless we want to track prev state.
                row.classList.add('status-viewed'); 
            }
            apiCall('/api/history', {id: id, action: 'undo_dismiss'});
        }
        
        function markAllVisible() {
            const newRows = document.querySelectorAll('tr.status-new');
            if (!newRows.length) {
                alert('No new items to mark.');
                return;
            }
            
            if (!confirm(`Mark $${newRows.length} items as seen?`)) return;
            
            newRows.forEach(row => {
                const id = row.id.replace('row-', '');
                markViewed(id, null);
            });
        }
    </script>
</head>
<body>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1>Property Search Results</h1>
        <button id="mark-all-btn" onclick="markAllVisible()">Mark All Visible as Seen</button>
    </div>
    <p>Generated report. Use the text areas to save notes.</p>
    <div id="content">
        $content
    </div>
</body>
</html>
"""
