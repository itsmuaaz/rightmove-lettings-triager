from utils import format_date, generate_google_maps_url, generate_tfl_url
import markdown
import html
from datetime import datetime

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
            
            # Timestamp and Refresh Logic
            timestamp_html = ""
            updated_at = p.get("commute_updated_at")
            prop_id = p.get("id")
            
            if updated_at:
                try:
                    dt = datetime.fromisoformat(updated_at)
                    time_str = dt.strftime("%H:%M")
                    timestamp_html = f'<div class="calc-timestamp">Updated: {time_str} <span style="cursor:pointer" onclick="refreshProperty(\'{prop_id}\')"><span class="refresh-icon">🔄</span></span></div>'
                except ValueError:
                    pass
            elif prop_id:
                 # Show refresh icon even if no timestamp yet
                 timestamp_html = f'<div class="calc-timestamp"><span style="cursor:pointer" onclick="refreshProperty(\'{prop_id}\')"><span class="refresh-icon">🔄</span> Refresh</span></div>'

            links_html = f'<div class="commute-links"><a href="{gmaps_link}" target="_blank">[GMaps]</a> <a href="{tfl_link}" target="_blank">[TfL]</a></div>'
            return f'<div class="commute-stack">{badges_html}{timestamp_html}{links_html}</div>'
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
        
        img_src = p.get("image_url")
        if img_src:
            image_html = f'<div class="img-container">{new_badge}<img src="{img_src}" class="prop-img" alt="Property"></div>'
        else:
            image_html = f'<div class="img-container">{new_badge}N/A</div>'
        
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
        shortlist_btn = f'<button class="btn btn-shortlist" onclick="markShortlisted(\'{prop_id}\', this)">⭐ Shortlist</button>'
        unshortlist_btn = f'<button class="btn btn-unshortlist" onclick="unshortlistProperty(\'{prop_id}\', this)">Remove ⭐</button>'
        dismiss_btn = f'<button class="btn btn-dismiss" onclick="dismissProperty(\'{prop_id}\', this)">Dismiss</button>'
        undo_btn = f'<button class="btn btn-undo" onclick="undoDismiss(\'{prop_id}\', this)">Undo</button>'
        
        actions_html = f'<div class="action-stack">{view_btn}{shortlist_btn}{unshortlist_btn}{dismiss_btn}{undo_btn}</div>'

        cells = [image_html, f"<strong>{p.get('price')}</strong>", commute_html, amenity_html, dist_str, notes_html, details, address, added_on, actions_html]
        row_content = "".join([f"<td>{c}</td>" for c in cells])
        return f'<tr class="{row_class}" id="row-{prop_id}">{row_content}</tr>'

    def _generate_shortlist_summary(self, properties):
        """Generates a summary section with links to shortlisted properties."""
        shortlisted = [p for p in properties if (p.get('history_status') or {}).get('status') == 'shortlisted']
        
        if not shortlisted:
            chips_html = (
                '<span style="color: #a0aec0; font-size: 0.9em;">'
                'No properties shortlisted yet. Click "⭐ Shortlist" '
                'on a property to add it here.</span>'
            )
        else:
            chips = []
            for p in shortlisted:
                addr = p.get('address', 'Unknown')
                # Shorten address for chip
                short_addr = addr.split(',')[0][:25]
                chips.append(f'<a href="#row-{p["id"]}" class="shortlist-chip" id="chip-{p["id"]}">{short_addr}</a>')
            chips_html = "".join(chips)

        return f"""
        <div class="summary-box" id="shortlist-summary">
            <h2>⭐ Shortlisted Properties</h2>
            <div class="shortlist-chips" id="summary-chips">
                {chips_html}
            </div>
        </div>
        """

    def generate_html_report(self, properties):
        """Generates the full HTML report directly."""
        summary = self._generate_shortlist_summary(properties)
        
        header_row = "".join([f"<th>{h}</th>" for h in self.headers])
        thead = f"<thead><tr>{header_row}</tr></thead>"
        
        rows = "".join([self._generate_html_row(p) for p in properties])
        tbody = f"<tbody>{rows}</tbody>"
        
        table = f"<table>{thead}{tbody}</table>"
        template = self.get_html_template()
        return template.replace('$content', summary + table)

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
        template = self.get_html_template()
        return template.replace('$content', html_table)

    def get_html_template(self):
        """Returns the HTML boilerplate with embedded CSS and JS."""
        with open("reporter_template.html", "r", encoding="utf-8") as f:
            return f.read()
