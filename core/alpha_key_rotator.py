import json
import os
import random

class AlphaKeyRotator:
    def __init__(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "keys.json")
        with open(file_path, "r") as f:
            self.keys = json.load(f).get("alpha_vantage_keys", [])
        self.index = 0

    def get_key(self):
        if not self.keys:
            raise ValueError("No Alpha Vantage keys available.")
        key = self.keys[self.index]
        self.index = (self.index + 1) % len(self.keys)
        return key
