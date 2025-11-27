import os
import json
import sys
from pathlib import Path

from paths import RESOURCES_DIR
from server.loggers import Loggers

ITEMS_PATH = RESOURCES_DIR / "items"


items = {}
try:
    items_paths = {
        "weapon": [ITEMS_PATH / "weapon" / p for p in os.listdir(ITEMS_PATH / "weapon") if p.endswith(".json")],
        "armor": [ITEMS_PATH / "armor" / p for p in os.listdir(ITEMS_PATH / "armor") if p.endswith(".json")],
        "jewelry": [ITEMS_PATH / "jewelry" / p for p in os.listdir(ITEMS_PATH / "jewelry") if p.endswith(".json")],
        "another": [ITEMS_PATH / "another" / p for p in os.listdir(ITEMS_PATH / "another") if p.endswith(".json")]
    }
except Exception as e:
    Loggers.game.error(f"Error with import items: {e}")
    sys.exit(1)

for group_type, item_paths in items_paths.items():
    for path in item_paths:
        with open(path, encoding="utf-8") as file:
            item_dict: dict = json.load(file)
            item_type = item_dict.get("_")
            if item_type != group_type:
                continue
            items.setdefault(item_dict.get("id"), item_dict)
Loggers.game.info("Successfull items import")