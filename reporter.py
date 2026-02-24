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
                    timestamp_html = f'<div class="calc-timestamp">Updated: {time_str} <span class="refresh-icon" onclick="refreshProperty(\'{prop_id}\')">🔄</span></div>'
                except ValueError:
                    pass
            elif prop_id:
                 # Show refresh icon even if no timestamp yet
                 timestamp_html = f'<div class="calc-timestamp"><span class="refresh-icon" onclick="refreshProperty(\'{prop_id}\')">🔄 Refresh</span></div>'

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
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Property Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 20px; color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: top; }}
        th {{ background-color: #f2f2f2; font-weight: 600; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        
        .prop-img {{ max-width: 150px; height: auto; border-radius: 4px; object-fit: cover; }}
        .img-container {{ position: relative; display: inline-block; }}
        
        /* Status Styles */
        tr.status-new {{ background-color: #e6fffa !important; border-left: 4px solid #38b2ac; }}
        tr.status-shortlisted {{ background-color: #fef3c7 !important; border-left: 4px solid #d69e2e; opacity: 1 !important; font-weight: 500; }}
        tr.status-viewed {{ opacity: 0.6; filter: grayscale(20%); }}
        tr.status-dismissed {{ opacity: 0.3; filter: grayscale(100%); max-height: 50px; overflow: hidden; }}
        /* Hide details when dismissed */
        tr.status-dismissed td {{ padding-top: 5px; padding-bottom: 5px; }}
        tr.status-dismissed .prop-img, tr.status-dismissed .commute-stack, tr.status-dismissed .note-input {{ display: none; }}
        
        /* Summary Section */
        .summary-box {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .summary-box h2 {{ margin-top: 0; font-size: 1.2em; color: #2d3748; display: flex; align-items: center; gap: 8px; }}
        .shortlist-chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .shortlist-chip {{ background: #fef3c7; color: #92400e; padding: 4px 12px; border-radius: 16px; font-size: 0.85em; font-weight: 600; text-decoration: none; border: 1px solid #fde68a; transition: all 0.2s; }}
        .shortlist-chip:hover {{ background: #fde68a; transform: translateY(-1px); }}
        .shortlist-chip::before {{ content: "⭐ "; }}
        
        /* Badges */
        .badge-new {{ position: absolute; top: -5px; right: -5px; background: #e53e3e; color: white; font-size: 0.7em; padding: 2px 6px; border-radius: 10px; font-weight: bold; box-shadow: 0 1px 3px rgba(0,0,0,0.2); z-index: 10; }}
        
        span[class^="badge-"] {{ padding: 4px 8px; border-radius: 4px; font-weight: 500; font-size: 0.9em; display: inline-block; }}
        .badge-green {{ background-color: #d4edda; color: #155724; }}
        .badge-amber {{ background-color: #fff3cd; color: #856404; }}
        .badge-red {{ background-color: #f8d7da; color: #721c24; }}
        .badge-grey {{ background-color: #e2e3e5; color: #383d41; }}

        .commute-stack {{ display: flex; flex-direction: column; gap: 4px; }}
        .commute-links {{ margin-top: 4px; font-size: 0.85em; }}
        
        /* Actions */
        .action-stack {{ display: flex; flex-direction: column; gap: 5px; }}
        .btn {{ padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9em; text-align: center; text-decoration: none; color: white; display: inline-block; }}
        .btn-view {{ background-color: #3182ce; }}
        .btn-dismiss {{ background-color: #718096; }}
        .btn-shortlist {{ background-color: #d69e2e; }}
        .btn-unshortlist {{ background-color: #ecc94b; color: #744210; }}
        .btn-undo {{ background-color: #38a169; display: none; }}
        
        /* Show Undo only when dismissed */
        tr.status-dismissed .btn-dismiss {{ display: none; }}
        tr.status-dismissed .btn-undo {{ display: inline-block; }}
        tr.status-dismissed .btn-view, tr.status-dismissed .btn-shortlist, tr.status-dismissed .btn-unshortlist {{ display: none; }}

        /* Button visibility based on status */
        tr.status-shortlisted .btn-shortlist {{ display: none; }}
        tr:not(.status-shortlisted) .btn-unshortlist {{ display: none; }}

        /* Notes */
        .note-input {{ width: 100%; height: 80px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; resize: vertical; font-family: inherit; box-sizing: border-box; }}
        .note-input:focus {{ border-color: #007bff; outline: none; }}
        
        a {{ color: #007bff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        
        /* Commute Timestamp and Refresh */
        .calc-timestamp {{ font-size: 0.7em; color: #718096; margin-top: 2px; }}
        .refresh-icon {{ cursor: pointer; font-size: 0.9em; margin-left: 4px; transition: transform 0.5s ease; display: inline-block; }}
        .refresh-icon:hover {{ transform: rotate(180deg); }}
        .refresh-icon.spinning {{ animation: spin 1s linear infinite; }}
        @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
        
        #refresh-all-btn {{ padding: 10px 20px; font-size: 1em; background-color: #38a169; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 10px; }}
        #refresh-all-btn:disabled {{ background-color: #cbd5e0; cursor: not-allowed; }}
    </style>
    <script>
        async function apiCall(endpoint, data) {{
            try {{
                const response = await fetch(endpoint, {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(data)
                }});
                if (!response.ok) return null;
                return await response.json();
            }} catch (err) {{
                console.error('API Error:', err);
                return null;
            }}
        }}

        function saveNote(propertyId, text) {{
            // Use fire-and-forget for notes, or handle error if needed
            fetch('/api/notes', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{id: propertyId, note: text}})
            }}).catch(err => console.error(err));
        }}

        async function refreshProperty(id) {{
            const row = document.getElementById('row-' + id);
            if (!row) return;
            
            const icon = row.querySelector('.refresh-icon');
            if (icon) icon.classList.add('spinning');
            
            const result = await apiCall('/api/refresh', {{id: id}});
            
            if (icon) icon.classList.remove('spinning');
            
            if (result && result.status === 'success' && result.property) {{
                const p = result.property;
                const commuteCell = row.cells[2];
                let html = '<div class="commute-stack">';
                
                const getBadgeClass = (m) => {{
                    if (m === null) return 'badge-grey';
                    if (m < 20) return 'badge-green';
                    if (m <= 40) return 'badge-amber';
                    return 'badge-red';
                }};
                
                if (p.commute_time !== null) {{
                    html += `<span class="${getBadgeClass(p.commute_time)}">${p.commute_time} mins 🚆</span>`;
                }}
                if (p.cycling_time !== null) {{
                    html += `<span class="${getBadgeClass(p.cycling_time)}">${p.cycling_time} mins 🚲</span>`;
                }}
                
                if (p.commute_updated_at) {{
                    const timeStr = new Date(p.commute_updated_at).toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
                    html += `<div class="calc-timestamp">Updated: ${timeStr} <span class="refresh-icon" onclick="refreshProperty('${id}')">🔄</span></div>`;
                }}
                
                const oldLinks = commuteCell.querySelector('.commute-links');
                if (oldLinks) html += oldLinks.outerHTML;
                
                html += '</div>';
                commuteCell.innerHTML = html;
            }} else {{
                alert('Failed to refresh property.');
            }}
        }}
        
        async function refreshAll() {{
            const btn = document.getElementById('refresh-all-btn');
            const originalText = btn.innerText;
            btn.disabled = true;
            btn.innerText = 'Refreshing...';
            
            const rows = document.querySelectorAll('tr.prop-row');
            const ids = Array.from(rows).map(r => r.id.replace('row-', ''));
            
            let count = 0;
            for (const id of ids) {{
                const row = document.getElementById('row-' + id);
                if (row.classList.contains('status-dismissed')) continue;

                btn.innerText = `Refreshing ${count + 1}/${ids.length}...`;
                await refreshProperty(id);
                count++;
                await new Promise(r => setTimeout(r, 500));
            }}
            
            btn.innerText = 'Refreshed!';
            setTimeout(() => {{
                btn.innerText = originalText;
                btn.disabled = false;
            }}, 2000);
        }}

        function updateShortlistSummary(id, action, address) {{
            const container = document.getElementById('summary-chips');
            if (!container) return;
            
            const existingChip = document.getElementById('chip-' + id);
            if (existingChip) existingChip.remove();
            
            if (action === 'shortlist') {{
                const shortAddr = (address || 'Unknown').split(',')[0].substring(0, 25);
                const chip = document.createElement('a');
                chip.href = '#row-' + id;
                chip.className = 'shortlist-chip';
                chip.id = 'chip-' + id;
                chip.textContent = shortAddr;
                container.appendChild(chip);
                
                if (container.innerText.includes('No properties shortlisted')) {{
                    container.innerHTML = '';
                    container.appendChild(chip);
                }}
            }} else if (action === 'dismiss') {{
                if (existingChip) existingChip.remove();
                if (container.children.length === 0) {{
                    container.innerHTML = '<span style="color: #a0aec0; font-size: 0.9em;">No properties shortlisted yet. Click "⭐ Shortlist" on a property to add it here.</span>';
                }}
            }}
        }}

        function markViewed(id, el) {{
            const row = document.getElementById('row-' + id);
            if (row) {{
                row.classList.remove('status-new');
                if (!row.classList.contains('status-shortlisted')) {{
                    row.classList.add('status-viewed');
                }}
                const badge = row.querySelector('.badge-new');
                if (badge) badge.remove();
            }}
            apiCall('/api/history', {{id: id, action: 'view'}});
            return true;
        }}

        function markShortlisted(id, btn) {{
            const row = document.getElementById('row-' + id);
            if (row) {{
                row.classList.remove('status-new', 'status-viewed');
                row.classList.add('status-shortlisted');
                const badge = row.querySelector('.badge-new');
                if (badge) badge.remove();
                
                const address = row.cells[7].innerText;
                updateShortlistSummary(id, 'shortlist', address);
            }}
            apiCall('/api/history', {{id: id, action: 'shortlist'}});
        }}

        function unshortlistProperty(id, btn) {{
            const row = document.getElementById('row-' + id);
            if (row) {{
                row.classList.remove('status-shortlisted');
                row.classList.add('status-viewed');
                updateShortlistSummary(id, 'dismiss');
            }}
            apiCall('/api/history', {{id: id, action: 'unshortlist'}});
        }}

        function dismissProperty(id, btn) {{
            const row = document.getElementById('row-' + id);
            if (row) {{
                row.classList.remove('status-new', 'status-viewed', 'status-shortlisted');
                row.classList.add('status-dismissed');
                updateShortlistSummary(id, 'dismiss');
            }}
            apiCall('/api/history', {{id: id, action: 'dismiss'}});
        }}

        function undoDismiss(id, btn) {{
            const row = document.getElementById('row-' + id);
            if (row) {{
                row.classList.remove('status-dismissed');
                row.classList.add('status-viewed'); 
            }}
            apiCall('/api/history', {{id: id, action: 'undo_dismiss'}});
        }}
        
        function markAllVisible() {{
            const newRows = document.querySelectorAll('tr.status-new');
            if (!newRows.length) {{
                alert('No new items to mark.');
                return;
            }}
            
            if (!confirm(`Mark ${newRows.length} items as seen?`)) return;
            
            newRows.forEach(row => {{
                const id = row.id.replace('row-', '');
                markViewed(id, null);
            }});
        }}
    </script>
</head>
<body>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1>Property Search Results</h1>
        <div>
            <button id="refresh-all-btn" onclick="refreshAll()">🔄 Refresh All Commutes</button>
            <button id="mark-all-btn" onclick="markAllVisible()">Mark All Visible as Seen</button>
        </div>
    </div>
    <p>Generated report. Use the text areas to save notes.</p>
    <div id="content">
        $content
    </div>
</body>
</html>
"""
