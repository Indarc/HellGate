from logging import Logger
import sys
import os
import json
from pathlib import Path
from typing import Optional

from db.executor import ItemsDB
from game.classes.items import *

from config import loggers


class ItemManager:
    def __init__(self, items_db_executor: ItemsDB, logger: Logger):
        self.item_classes = {
            "weapon": Weapon,
            "armor": Armor,
            "jewelry": Jewelry,
            "bag": Bag,
            "material": Material,
            "another": Item
        }
        self.items: dict[str, Item] = {}
        self.items_db_executor = items_db_executor
        self.logger = logger

    async def add(self, item_object: Item):
        if not item_object.identificator:
            self.logger.warning("To add new item to DB, item object must have uniq Identificator.")
            return
        if await self.get(item_object.identificator):
            self.logger.warning(f"Item with Identificator [{item_object.identificator}] is already exist in DB.")
            return
        await self.items_db_executor.add(item_object=item_object)
        self.logger.info(f"Created new item in ITEM_DB with identificator={item_object.identificator}")
    
    async def get(self, identificator: str) -> Optional[Item | EquipItem]:
        """Return item object by item id"""
        item_local = self.items.get(identificator)
        if item_local:
            return item_local
        item_model = await self.items_db_executor.get(identificator)
        if not item_model:
            self.logger.warning(f"Can`t get item with identificator=[{identificator}]. Item does not exist.")
            return
        item_dict: dict = item_model.data
        if not item_dict:
            self.logger.warning(f"Item [{item_model.identificator}] from DB have not data field.")
            return
        item_type = item_dict.get("type")
        if not item_type:
            self.logger.error(f"Item dict have not type field: {item_dict}")
            return
        item_class: Optional[Item] = self.item_classes.get(item_type)
        if not item_class:
            self.logger.error(f"Can`t find Item class for [{item_type}]")
            return
        item: Item = item_class(data=item_dict)
        if self.items.__len__() < 100:
            self.items.update({item.identificator: item})
        else:
            lambda: (k := next(iter(self.items)), self.items.pop(k))
            self.items.update({item.identificator: item})
        return item

    async def update(self, item_object: Item) -> bool:
        item_local = self.items.pop(item_object.identificator, None)
        if item_local:
            self.logger.info(f"Remove item [{item_local.identificator}] from local memory")
        if not await self.items_db_executor.update(item_object):
            self.logger.error("Failde to update item in DB.")
            return False
        return True

    def dict_to_item(self, item_dict: dict) -> Optional[Item]:
        """Convert item dict to item object"""
        item_identificator = item_dict.get("identificator")
        item_type = item_dict.get("type")
        if not item_identificator or not item_type:
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