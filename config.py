import os

def load_config():
    """Load configuration from environment variables and defaults."""
    return {
        "TFL_APP_ID": os.getenv("TFL_APP_ID"),
        "TFL_APP_KEY": os.getenv("TFL_APP_KEY"),
        "GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY"),
        
        # Scoring Configuration
        "SCORING_WEIGHTS": {
            "price": 0.3,
            "commute": 0.4,
            "vibe": 0.2,
            "freshness": 0.1
        },
        "MAX_COMMUTE_MINS": 60,
        "FRESHNESS_DECAY_DAYS": 7
    }
