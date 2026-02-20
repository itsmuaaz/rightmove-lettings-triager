import os

def load_config():
    """Load configuration from environment variables."""
    return {
        "TFL_APP_ID": os.environ.get("TFL_APP_ID"),
        "TFL_APP_KEY": os.environ.get("TFL_APP_KEY"),
        "GOOGLE_MAPS_API_KEY": os.environ.get("GOOGLE_MAPS_API_KEY"),
    }
