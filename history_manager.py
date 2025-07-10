import json
import os
from datetime import datetime
from config import MAX_HISTORY_ITEMS

class HistoryManager:
    def __init__(self):
        self.history_file = "excuse_history.json"
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history[-MAX_HISTORY_ITEMS:], f)

    def add_excuse(self, excuse, scenario, tags=[]):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "excuse": excuse,
            "scenario": scenario,
            "tags": tags
        }
        self.history.append(entry)
        self._save_history()

    def get_history(self, limit=10):
        return self.history[-limit:]

    def get_favorites(self):
        return [excuse for excuse in self.history if "favorite" in excuse.get("tags", [])]

    def toggle_favorite(self, timestamp):
        for excuse in self.history:
            if excuse["timestamp"] == timestamp:
                if "favorite" in excuse.get("tags", []):
                    excuse["tags"].remove("favorite")
                else:
                    if "tags" not in excuse:
                        excuse["tags"] = []
                    excuse["tags"].append("favorite")
                self._save_history()
                return True
        return False