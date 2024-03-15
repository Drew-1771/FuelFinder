from pathlib import Path
import json


class DataManager:
    """Manages the token for the bot stored in the token.json file"""

    def __init__(self, path: Path):
        self._path = path

    def write(self, data: dict) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(data, f)
