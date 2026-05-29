import json
import os
import shutil
try:
    import tomllib
except ImportError:
    pass # Should be Python 3.11+
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_file: str = "config.toml", defaults: Dict[str, Any] = None):
        self.config_file = config_file
        self.defaults = defaults or {}

    def _deep_merge(self, dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """Deeply merges dict2 into dict1."""
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_file):
            template_path = f"{self.config_file}.template"
            if os.path.exists(template_path):
                shutil.copyfile(template_path, self.config_file)
            else:
                return self.defaults.copy()

        config = {}
        try:
            with open(self.config_file, 'rb') as f:
                config = tomllib.load(f)
        except Exception:
            # Fallback if invalid TOML
            return self.defaults.copy()

        # Merge defaults into the loaded TOML config
        merged_config = self._deep_merge(self.defaults, config)

        # Environment variable overrides
        if "credentials" not in merged_config:
            merged_config["credentials"] = {}
            
        if os.getenv("TFL_APP_ID"):
            merged_config["credentials"]["tfl_app_id"] = os.getenv("TFL_APP_ID")
        if os.getenv("TFL_APP_KEY"):
            merged_config["credentials"]["tfl_app_key"] = os.getenv("TFL_APP_KEY")

        return merged_config

    def save_config(self, weights: Dict[str, float]):
        """Updates the [scoring.weights] section in the TOML file, preserving comments."""
        normalized = self.normalize_weights(weights)
        if not os.path.exists(self.config_file):
            return

        try:
            with open(self.config_file, 'r') as f:
                lines = f.readlines()

            # Find the [scoring.weights] section
            in_weights_section = False
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('[') and stripped.endswith(']'):
                    if stripped == '[scoring.weights]':
                        in_weights_section = True
                    else:
                        in_weights_section = False
                    continue

                if in_weights_section and '=' in line and not stripped.startswith('#'):
                    key = line.split('=')[0].strip()
                    if key in normalized:
                        # Replace the line, preserving original indentation
                        indent = line[:len(line) - len(line.lstrip())]
                        lines[i] = f"{indent}{key} = {normalized[key]}\n"

            with open(self.config_file, 'w') as f:
                f.writelines(lines)
        except IOError:
            pass

    def normalize_weights(self, weights: Dict[str, float]) -> Dict[str, float]:
        total = sum(weights.values())
        if total == 0:
            return self.defaults.get("scoring", {}).get("weights", {})
        
        return {k: v / total for k, v in weights.items()}
