from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils import format_date, generate_google_maps_url, generate_tfl_url, extract_numeric_price
from datetime import datetime
import os

class Reporter:
    """Generates HTML reports for property search results using Jinja2."""

    def __init__(self, template_dir="templates"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def _calculate_price_boundaries(self, properties):
        """Calculates the minimum and maximum numeric prices in the result set."""
        valid_prices = []
        for p in properties:
            num = extract_numeric_price(p.get('price'))
            if num is not None:
                valid_prices.append(num)
        
        if not valid_prices:
            return None, None
            
        return min(valid_prices), max(valid_prices)

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
                pass
        return processed

    def _get_smart_score_bg_color(self, score):
        """Returns the HSL color string for the smart score badge."""
        if score is None:
            return "#D1D5DB" # gray-300
        
        try:
            val = round(score)
            # Threshold Gradient Logic
            # 80-100: Green (120)
            # 0-20: Red (0)
            # 20-80: Linear
            
            if val >= 80:
                hue = 120
            elif val <= 20:
                hue = 0
            else:
                ratio = (val - 20) / 60
                hue = int(120 * ratio)
            
            return f"hsl({hue}, 100%, 40%)" # Slightly darker for text readability (40% lightness)
        except (ValueError, TypeError):
             return "#D1D5DB"

    def _get_vibe_class(self, score):
        """Returns the Tailwind color class for the vibe text."""
        if score is None:
            return "text-text-tertiary"
        
        try:
            val = float(score)
            if val >= 8:
                return "text-state-good"
            elif val >= 5:
                return "text-state-avg"
            else:
                return "text-state-bad"
        except (ValueError, TypeError):
             return "text-text-tertiary"

    def _enrich_property(self, p, min_price=None, max_price=None):
        """Enriches a property dict with display-ready fields."""
        p = p.copy()
        
        # Price Indicator
        if min_price is not None and max_price is not None:
            price_val = extract_numeric_price(p.get('price'))
            if price_val is not None:
                if min_price == max_price:
                    hue = 60
                else:
                    ratio = (price_val - min_price) / (max_price - min_price)
                    ratio = max(0.0, min(1.0, ratio))
                    hue = int(120 * (1 - ratio))
                
                p['price_indicator_color'] = f"hsl({hue}, 100%, 45%)"

        # Commute
        is_processed = 'commute_time' in p
        commute_mins = p.get("commute_time")
        
        if not is_processed:
            p['commute_time'] = "Loading..."
            p['commute_color_class'] = "text-gray-400 italic"
        else:
            p['commute_color_class'] = self._get_commute_class(commute_mins)
            p['commute_time'] = commute_mins if commute_mins is not None else "N/A"
            
            commute_fares = p.get('commute_fares')
            if commute_fares:
                peak = commute_fares.get('peak')
                off_peak = commute_fares.get('off_peak')
                total_cost = commute_fares.get('total_cost')
                cost = commute_fares.get('cost')
                
                cost_str = None
                if peak and off_peak:
                    cost_str = f"£{peak/100:.2f} / £{off_peak/100:.2f}"
                elif total_cost:
                    cost_str = f"£{total_cost/100:.2f}"
                elif cost:
                    cost_str = f"£{cost/100:.2f}"
                elif peak:
                     cost_str = f"£{peak/100:.2f}"
                elif off_peak:
                     cost_str = f"£{off_peak/100:.2f}"
                
                if cost_str:
                    p['commute_cost_display'] = cost_str
        
        cycling_mins = p.get("commute_cycling")
        if not is_processed:
             p['cycling_time'] = "Loading..."
             p['cycling_color_class'] = "text-gray-400 italic"
        else:
             p['cycling_color_class'] = self._get_commute_class(cycling_mins)
             p['cycling_time'] = cycling_mins if cycling_mins is not None else "N/A"

        # Links
        origin_address = p.get('address', '')
        origin_coords = None
        if p.get('latitude') and p.get('longitude'):
            origin_coords = (p.get('latitude'), p.get('longitude'))
        
        raw_url = p.get('url', '')
        if raw_url.startswith('http'):
            p['link'] = raw_url
        else:
            p['link'] = f"https://www.rightmove.co.uk{raw_url}"

        p['google_maps_link'] = generate_google_maps_url(origin_address)
        p['tfl_link'] = generate_tfl_url(origin_address, origin_coords)
        
        # Amenities
        if 'nearby_amenities' in p:
            p['amenities'] = self._process_amenities(p.get('nearby_amenities'))
        else:
            p['amenities'] = []

        # Dates/Formatting
        p['added_on'] = format_date(p.get("published_on"))
        
        if 'price' in p:
             p['price_pcm'] = p['price']
             p['price_pw'] = "N/A"

        # Status
        history = p.get('history_status', {}) or {}
        p['status'] = history.get('status', 'new')
        p['is_new'] = (p['status'] == 'new')
        
        if 'id' not in p and 'url' in p:
             p['id'] = str(hash(p['url']))

        p['notes'] = p.get('note') or ''

        if 'image_url' in p and 'images' not in p:
            p['images'] = [p['image_url']]
        
        # Vibe
        vibe = p.get('vibe')
        if vibe:
            score = vibe.get('score')
            p['vibe_score'] = score
            p['vibe_summary'] = vibe.get('summary', 'Unknown')
            p['vibe_safety'] = vibe.get('safety', 'Unknown')
            p['vibe_color_class'] = self._get_vibe_class(score)
        else:
             p['vibe_score'] = "N/A"
             p['vibe_summary'] = "Unknown"
             p['vibe_safety'] = "Unknown"
             p['vibe_color_class'] = "text-text-tertiary"
        
        # Smart Score
        smart_score = p.get('smart_score')
        base_classes = "inline-flex items-center justify-center h-8 w-8 rounded-full text-sm font-bold shadow-sm text-white"
        
        if smart_score is not None:
            score_val = round(smart_score)
            p['smart_score'] = score_val
            p['smart_score_badge_class'] = base_classes
            p['smart_score_bg_color'] = self._get_smart_score_bg_color(score_val)
        else:
            p['smart_score'] = "N/A"
            p['smart_score_badge_class'] = base_classes
            p['smart_score_bg_color'] = self._get_smart_score_bg_color(None)

        return p

    def generate_report(self, properties, shortlist=None, filters=None, processed_count=None, total_count=None, sort_by='smart_score', order='desc', mode='min'):
        """Generates the HTML report."""
        template = self.env.get_template("report.html")
        
        min_price, max_price = self._calculate_price_boundaries(properties)
        
        enriched_properties = [self._enrich_property(p, min_price=min_price, max_price=max_price) for p in properties]
        
        enriched_shortlist = []
        if shortlist:
             enriched_shortlist = [self._enrich_property(p, min_price=min_price, max_price=max_price) for p in shortlist]
        elif shortlist is None:
             enriched_shortlist = [p for p in enriched_properties if p.get('status') == 'shortlisted']

        return template.render(
            properties=enriched_properties,
            shortlist=enriched_shortlist,
            filters=filters,
            processed_count=processed_count,
            total_count=total_count,
            sort_by=sort_by,
            order=order,
            mode=mode,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
