import sys
import os
import json
from pathlib import Path
from typing import Optional

from game.classes.items import *

from config import loggers


class ItemManager:
    def __init__(self, items_path: Path):
        self.items_path = items_path
        self.item_classes = {
            "weapon": Weapon,
            "armor": Armor,
            "jewelry": Jewelry,
            "bag": Bag,
            "another": Item
        }
        self.items: dict[int, Item] = self.__load_items()
    
    def get_item(self, item_id: int) -> Optional[Item | EquipItem]:
        """Return item object by item id"""
        return self.items.get(item_id)

    def dict_to_item(self, item_dict: dict) -> Optional[Item]:
        """Convert item dict to item object"""
        item_id = item_dict.get("id")
        item_type = item_dict.get("_")
        if not item_id or not item_type:
            loggers.game.warning(f"Item id or type not found in dict: {item_dict}")
            return None
        item_class = self.item_classes.get(item_type)
        if not item_class:
            loggers.game.warning(f"Undefined item type: {item_type} in dict: {item_dict}")
            return None
        item = item_class(data=item_dict)
        return item
    
    def dti(self, item_dict: dict) -> Optional[Item]:
        """Overload for dict_to_item method"""
        return self.dict_to_item(item_dict=item_dict)

    def __load_items(self) -> dict:
        items = {}
        try:
            items_path = {
                "weapon": [self.items_path / "weapon" / p for p in os.listdir(self.items_path / "weapon") if p.endswith(".json")],
                "armor": [self.items_path / "armor" / p for p in os.listdir(self.items_path / "armor") if p.endswith(".json")],
                "jewelry": [self.items_path / "jewelry" / p for p in os.listdir(self.items_path / "jewelry") if p.endswith(".json")],
                "another": [self.items_path / "another" / p for p in os.listdir(self.items_path / "another") if p.endswith(".json")]
            }
        except Exception as e:
            loggers.game.error(f"Error with import items: {e}")
            sys.exit(1)

        for group_type, item_paths in items_path.items():
            for path in item_paths:
                with open(path, encoding="utf-8") as file:
                    item_dict: dict = json.load(file)
                    item_type = item_dict.get("item_type")
                    if not item_type:
                        loggers.game.warning(f"Item type not found in file {path}")
                        continue
                    if group_type != "another":
                        if item_type != group_type and item_type not in self.item_classes.keys():
                            loggers.game.warning(f"Item type mismatch: {item_type} != {group_type} in file {path}")
                            continue
                    item_class = self.item_classes.get(item_type)
                    if not item_class:
                        loggers.game.warning(f"Undefined item type: {item_type} in file {path}")
                        continue
                    item = item_class(data=item_dict)
                    items.update({item_dict.get("id"): item})
        loggers.game.info("Successfull items import")
        return items