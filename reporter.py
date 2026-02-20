from utils import format_date
import markdown
from string import Template

class Reporter:
    def __init__(self):
        self.headers = ["Image", "Price", "Commute", "Distance", "Details", "Address", "Added On", "Link"]

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

    def _generate_row(self, p):
        """Generates a Markdown table row for a property."""
        image_html = f'<img src="{p.get("image_url")}" class="prop-img" alt="Property">' if p.get("image_url") else "N/A"
        
        commute_mins = p.get("commute_time")
        commute_class = self._get_commute_class(commute_mins)
        commute_text = f"{commute_mins} mins" if commute_mins is not None else "N/A"
        commute_html = f'<span class="{commute_class}">{commute_text}</span>'
        
        dist_val = p.get("distance")
        dist_str = f"{dist_val:.2f} mi" if dist_val else "N/A"
        
        details = f"{p.get('bedrooms', 0)} bed {p.get('type', 'Property')}"
        added_on = format_date(p.get("published_on"))
        
        link = f"https://www.rightmove.co.uk{p.get('url', '')}"
        link_html = f'[View]({link})'

        return f"| {image_html} | **{p.get('price')}** | {commute_html} | {dist_str} | {details} | {p.get('address')} | {added_on} | {link_html} |"

    def generate_markdown(self, properties):
        """Generates the full Markdown report."""
        header_row = "| " + " | ".join(self.headers) + " |\n"
        separator_row = "| " + " | ".join(["---"] * len(self.headers)) + " |\n"
        
        md = header_row + separator_row
        
        for p in properties:
            md += self._generate_row(p) + "\n"
            
        return md

    def convert_to_html(self, md_content):
        """Converts Markdown content to a styled HTML report."""
        html_table = markdown.markdown(md_content, extensions=['tables'])
        template = Template(self.get_html_template())
        return template.substitute(content=html_table)

    def get_html_template(self):
        """Returns the HTML boilerplate with embedded CSS."""
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
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: middle; }
        th { background-color: #f2f2f2; font-weight: 600; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        
        .prop-img { max-width: 150px; height: auto; border-radius: 4px; object-fit: cover; }
        
        /* Commute Badges */
        span[class^="badge-"] { padding: 4px 8px; border-radius: 4px; font-weight: 500; font-size: 0.9em; display: inline-block; }
        .badge-green { background-color: #d4edda; color: #155724; }
        .badge-amber { background-color: #fff3cd; color: #856404; }
        .badge-red { background-color: #f8d7da; color: #721c24; }
        .badge-grey { background-color: #e2e3e5; color: #383d41; }
        
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Property Search Results</h1>
    <p>Generated report.</p>
    <div id="content">
        $content
    </div>
</body>
</html>
"""
