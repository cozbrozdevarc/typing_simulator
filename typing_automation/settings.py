import json
import os
from typing import Dict, Any

class Settings:
    DEFAULT_SETTINGS = {
        'min_typing_speed': 0.3,
        'max_typing_speed': 0.7,
        'min_chunk_size': 10,
        'max_chunk_size': 20,
        'min_pause': 1,
        'max_pause': 5,
        'error_rate': 0.1,
        'correction_delay': 0.5,
        'max_error_chars': 2
    }

    def __init__(self):
        self.settings = self.DEFAULT_SETTINGS.copy()
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.settings_file = os.path.join(project_root, 'typing_settings.json')
        self.load_settings()

    def load_settings(self) -> None:
        try:
            with open(self.settings_file, 'r') as f:
                content = f.read().strip()
                if content:
                    loaded_settings = json.loads(content)
                    # Get settings from the "Actual Settings" section
                    actual_settings = next(
                        (v for k, v in loaded_settings.items() if "Actual Settings" in k),
                        None
                    )
                    if actual_settings:
                        self.settings.update(actual_settings)
                    else:
                        self.save_settings()
                else:
                    self.save_settings()
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_settings()

    def save_settings(self) -> None:
        with open(self.settings_file, 'w') as f:
            # Create settings file with documentation structure
            settings_json = {
                "// Settings Documentation": {
                    setting: {
                        "description": "See documentation above for details",
                        "recommended_range": "See documentation above",
                        "example": "See documentation above"
                    }
                    for setting in self.settings.keys()
                },
                "// Actual Settings (modify these values)": self.settings,
                "// Preset Configurations (copy values to settings above)": {
                    "fast_accurate": {
                        "min_typing_speed": 0.1,
                        "max_typing_speed": 0.3,
                        "error_rate": 0.05,
                        "min_chunk_size": 15,
                        "max_chunk_size": 30,
                        "min_pause": 1,
                        "max_pause": 3
                    },
                    "natural_human": {
                        "min_typing_speed": 0.3,
                        "max_typing_speed": 0.7,
                        "error_rate": 0.2,
                        "min_chunk_size": 10,
                        "max_chunk_size": 20,
                        "min_pause": 1,
                        "max_pause": 5
                    },
                    "learning_typist": {
                        "min_typing_speed": 0.5,
                        "max_typing_speed": 1.0,
                        "error_rate": 0.3,
                        "min_chunk_size": 5,
                        "max_chunk_size": 15,
                        "min_pause": 2,
                        "max_pause": 7
                    }
                }
            }
            json.dump(settings_json, f, indent=4)

    def get(self, key: str) -> Any:
        return self.settings.get(key)

    def update(self, new_settings: Dict[str, Any]) -> None:
        self.settings.update(new_settings)
        self.save_settings()
