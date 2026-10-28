import json
import os


class Storage:
    def __init__(self, filepath="expenses.json"):
        self.filepath = filepath

    def load(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []

    def save(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)
