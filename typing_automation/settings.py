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
        'max_pause': 5
    }

    def __init__(self):
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.settings_file = 'typing_mocker/typing_settings.json'
        self.load_settings()

    def load_settings(self) -> None:
        try:
            with open(self.settings_file, 'r') as f:
                self.settings.update(json.load(f))
        except FileNotFoundError:
            self.save_settings()

    def save_settings(self) -> None:
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key: str) -> Any:
        return self.settings.get(key)

    def update(self, new_settings: Dict[str, Any]) -> None:
        self.settings.update(new_settings)
        self.save_settings()