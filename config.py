"""Configuration module for loading environment variables."""

import os
from typing import Dict, Optional

def load_config() -> Dict[str, Optional[str]]:
    """Loads configuration from environment variables.

    Returns:
        A dictionary containing TfL and Google Maps API keys.
    """
    return {
        "TFL_APP_ID": os.environ.get("TFL_APP_ID"),
        "TFL_APP_KEY": os.environ.get("TFL_APP_KEY"),
        "GOOGLE_MAPS_API_KEY": os.environ.get("GOOGLE_MAPS_API_KEY"),
    }
