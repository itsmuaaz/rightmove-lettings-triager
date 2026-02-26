import os
from config_manager import ConfigManager

def load_config():
    """Load configuration from environment variables and defaults."""
    
    # New defaults as per spec
    defaults = {
        "price": 0.3,
        "commute": 0.3,
        "vibe": 0.3,
        "freshness": 0.1
    }
    
    manager = ConfigManager(config_file=".scoring_config.json", defaults=defaults)
    scoring_weights = manager.load_config()

    return {
        "TFL_APP_ID": os.getenv("TFL_APP_ID"),
        "TFL_APP_KEY": os.getenv("TFL_APP_KEY"),
        "GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY"),
        
        # Scoring Configuration
        "SCORING_WEIGHTS": scoring_weights,
        "MAX_COMMUTE_MINS": 60,
        "FRESHNESS_DECAY_DAYS": 7
    }
