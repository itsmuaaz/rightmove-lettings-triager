from utils import format_date

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
