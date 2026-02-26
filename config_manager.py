import json
import os
from typing import Dict

class ConfigManager:
    def __init__(self, config_file: str, defaults: Dict[str, float]):
        self.config_file = config_file
        self.defaults = defaults

    def load_config(self) -> Dict[str, float]:
        if not os.path.exists(self.config_file):
            return self.defaults
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def save_config(self, weights: Dict[str, float]):
        normalized = self.normalize_weights(weights)
        try:
            with open(self.config_file, 'w') as f:
                json.dump(normalized, f, indent=2)
        except IOError:
            pass

    def normalize_weights(self, weights: Dict[str, float]) -> Dict[str, float]:
        total = sum(weights.values())
        if total == 0:
            return self.defaults
        
        return {k: v / total for k, v in weights.items()}
