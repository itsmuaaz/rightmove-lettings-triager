from typing import Dict, Any, Optional
from utils import get_days_since, extract_numeric_price
from config import load_config

class SmartScorer:
    """Calculates a 'Smart Score' (0-100) for a property based on weighted criteria."""

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        config = load_config()
        
        self.weights = weights or config.get("SCORING_WEIGHTS")
        self.max_commute = config.get("MAX_COMMUTE_MINS", 60)
        self.freshness_decay = config.get("FRESHNESS_DECAY_DAYS", 7)

    def calculate_score(self, property_data: Dict[str, Any], global_stats: Dict[str, float]) -> Dict[str, Any]:
        """Calculates the weighted score for a property.

        Args:
            property_data: Dictionary containing property details.
            global_stats: Dictionary containing 'min_price' and 'max_price' context.

        Returns:
            A dictionary containing the 'total' score (0-100) and a 'breakdown' dict.
        """
        # 1. Normalize Components (0-100)
        # Price
        price_val = extract_numeric_price(property_data.get('price'))
        price_score = self._normalize_price(price_val, global_stats.get('min_price'), global_stats.get('max_price'))

        # Commute
        commute_val = property_data.get('commute_time')
        commute_score = self._normalize_commute(commute_val)

        # Vibe
        vibe_data = property_data.get('vibe')
        vibe_val = vibe_data.get('score') if vibe_data else property_data.get('vibe_score')
        vibe_score = self._normalize_vibe(vibe_val)

        # Freshness
        pub_date = property_data.get('published_on')
        days_since = get_days_since(pub_date)
        freshness_score = self._normalize_freshness(days_since)

        # If any of the core parameters (Price, Commute, or Vibe) are missing, we do not calculate the total score (returns None)
        if price_score is None or commute_score is None or vibe_score is None:
            return {
                "total": None,
                "breakdown": {
                    "price": price_score,
                    "commute": commute_score,
                    "vibe": vibe_score,
                    "freshness": freshness_score
                }
            }

        # 2. Redistribute Weights for Missing Data
        valid_components = {}
        missing_weight = 0.0
        
        # Check each component
        components = {
            "price": price_score,
            "commute": commute_score,
            "vibe": vibe_score,
            "freshness": freshness_score
        }

        total_valid_weight = 0.0
        
        for key, val in components.items():
            weight = self.weights.get(key, 0)
            if val is not None:
                valid_components[key] = (val, weight)
                total_valid_weight += weight
            else:
                missing_weight += weight

        # 3. Calculate Final Score
        final_score = 0.0
        breakdown = {}

        if total_valid_weight > 0:
            # Scale factor to redistribute missing weight proportionally
            # e.g., if total_valid_weight is 0.6, scale_factor is 1 / 0.6 = 1.666
            scale_factor = 1.0 / total_valid_weight
            
            for key, (score, weight) in valid_components.items():
                # Apply weight and scale up
                weighted_contribution = score * weight * scale_factor
                final_score += weighted_contribution
                breakdown[key] = weighted_contribution
        else:
            final_score = 0.0

        # Fill missing keys in breakdown with None
        for key in components:
            if key not in breakdown:
                breakdown[key] = None

        return {
            "total": round(final_score, 1),
            "breakdown": breakdown
        }

    def _normalize_price(self, price: Optional[float], min_p: Optional[float], max_p: Optional[float]) -> Optional[float]:
        """Normalizes price relative to min/max. Cheapest = 100."""
        if price is None or min_p is None or max_p is None:
            return None
        
        if min_p == max_p:
            return 100.0 # Only one price or all same
            
        # Linear interpolation: (price - min) / (max - min) gives 0 (cheap) to 1 (expensive)
        # We want 1 (cheap) to 0 (expensive), so 1 - ...
        ratio = (price - min_p) / (max_p - min_p)
        ratio = max(0.0, min(1.0, ratio)) # Clamp
        
        return (1.0 - ratio) * 100.0

    def _normalize_commute(self, minutes: Optional[float]) -> Optional[float]:
        """Normalizes commute time. <= 20 mins = 100, >= 60 mins = 0."""
        if minutes is None:
            return None
            
        try:
            mins = float(minutes)
        except (ValueError, TypeError):
            return None

        if mins <= 20:
            return 100.0
        if mins >= self.max_commute:
            return 0.0
            
        # Linear decay between 20 and 60
        # Range is 40 mins (60 - 20)
        # Value is (60 - mins) / 40
        return ((self.max_commute - mins) / (self.max_commute - 20)) * 100.0

    def _normalize_vibe(self, score: Optional[int]) -> Optional[float]:
        """Normalizes vibe score (1-10) to 0-100."""
        if score is None:
            return None
            
        try:
            val = int(score)
        except (ValueError, TypeError):
            return None
            
        # Map 1-10 to 10-100? Or 0-100?
        # Let's map 1->10, 10->100
        return float(max(0, min(100, val * 10)))

    def _normalize_freshness(self, days: Optional[int]) -> Optional[float]:
        """Normalizes freshness. 0 days = 100, >= 7 days = 0."""
        if days is None:
            return None
            
        if days <= 0:
            return 100.0
        if days >= self.freshness_decay:
            return 0.0
            
        # Linear decay
        return ((self.freshness_decay - days) / self.freshness_decay) * 100.0
