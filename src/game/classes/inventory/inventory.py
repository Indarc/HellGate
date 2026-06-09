from typing import Optional

from game.classes.items import Item
from game.classes.items import EquipItem
from game.classes.items import Weapon
from game.classes.items import Armor
from game.classes.items import Jewelry
from config import loggers

from .error_class import ItemRemoveError, DontEnoughSlotsError, SlotOverloadError


class Inventory:
    sorter = {
        "another": Item,
        "weapon": Weapon,
        "armor": Armor,
        "jewelry": Jewelry
    }
    def __init__(self, max_space: int = 10, data: Optional[dict] = None):
        if data:
            self.space: int = data.get("space", max_space)
            self.max_space: int = data.get("max_space", max_space)
            self.slots: dict[int, Slot] = {}
            slots_dict: dict = data.get("slots", {})
            if slots_dict:
                for slot_id, slot_dict in slots_dict.items():
                    self.slots.setdefault(int(slot_id), Slot(slot_index=int(slot_id), data=slot_dict))
            else:
                self.slots: dict[int, Slot] = {x : Slot(slot_index=x) for x in range(0, max_space)}
        else:
            self.space = max_space
            self.max_space = max_space
            self.slots: dict[int, Slot] = {x : Slot(slot_index=x) for x in range(0, max_space)}
    
    def get_free_space(self) -> int:
        return self.space

    def add_item(self, item: Item, count: int = 1) -> bool:
        if self.get_free_space() == 0:
            # TODO send message to player about that
            raise DontEnoughSlotsError()
        for i, slot in self.slots.items():
            if item.stacked and slot.item and slot.item.id == item.id:
                try:
                    self.slots[i].add_item(item=item, count=count)
                except SlotOverloadError as e:
                    loggers.inventory_logger.warning(f"Failed to add item with id {item.id} to slot [{i}] because of {e.value}")
                    # TODO send message to player about that
                    raise SlotOverloadError()
                return True
            elif not item.stacked and not slot.item:
                self.slots[i].add_item(item=item, count=count)
                self.space -= 1
                return True
        for i, slot in self.slots.items():
            if not slot.item:
                try:
                    self.slots[i].add_item(item=item, count=count)
                    self.space -= 1
                except SlotOverloadError as e:
                    loggers.inventory_logger.warning(f"Failed to add item with id {item.id} to slot [{i}] because of {e.value}")
                    # TODO send message to player about that
                    raise SlotOverloadError()
                return True
        return False
    
    def get_slot(self, slot_id) -> Optional["Slot"]:
        slot = self.slots.get(slot_id, None)
        if not slot or not slot.item:
            loggers.inventory_logger.warning(f"Item in slot [{slot_id}] is [None].")
            return None

    def extract_item(self, slot_id: int, extract_count: int=1) -> Optional[tuple[Item | EquipItem, int]]:
        """Extract part of item stack from inventory and return it as tuple (item, count) or None if something went wrong"""
        # Полезно для передачи части стека предметов, например при продаже или крафте
        slot = self.slots.get(slot_id)
        if not slot or not slot.item:
            loggers.inventory_logger.warning(f"Item in slot [{slot_id}] is [None]")
            return None
        if extract_count <= 0:
            loggers.inventory_logger.warning(f"Invalid extract count: {extract_count}")
            return None
        item, count = slot.get_item()
        if not item:
            loggers.inventory_logger.warning(f"Item in slot [{slot_id}] is [None]")
            return None
        if not item.stacked and extract_count > 1:
            loggers.inventory_logger.warning(f"Trying to extract more than 1 non-stacked item from slot [{slot_id}]")
            return None
        elif item.stacked and extract_count > count:
            loggers.inventory_logger.warning(f"Trying to extract more items than in slot [{slot_id}]")
            return None
        elif item.stacked and extract_count == count:
            self.slots[slot_id].clear_slot()
            self.space += 1
            return (item, count)
        elif item.stacked and extract_count <= count:
            self.slots[slot_id].count -= extract_count
            return (item, extract_count)
        elif not item.stacked and extract_count == 1:
            self.slots[slot_id].clear_slot()
            self.space += 1
            return (item, 1)        
    
    def to_dict(self) -> dict:
        slots = {}
        for i, slot in self.slots.items():
            slots.setdefault(i, slot.to_dict())
        inv_dict = {
            "max_space": self.max_space,
            "space": self.space,
            "slots": slots
        }
        return inv_dict

class Slot:
    def __init__(self, slot_index, item: Optional["Item"]=None, count: int=0, data: Optional[dict]=None):
        self.max_count = 99 # ограничение на колличество стакаемых предметов в одном слоте, может быть изменено в будущем для разных типов предметов
        if data:
            self.slot_index: int = slot_index
            item_dict: dict = data.get("item", {})
            if item:
                item_type = item_dict.get("_")
                if item_type == "weapon":
                    self.item = Weapon(data=item_dict)
                elif item_type == "armor":
                    self.item = None
                elif item_type == "jewelry":
                    self.item = None
                elif item_type == "another":
                    self.item = Item(data=data)
                else:
                    self.item = slot_index
            else:
                self.item = None
            self.count: int = data.get("count", 0)
        else:
            self.slot_index = slot_index
            self.item = item
            self.count = count
    
    def add_item(self, item: Item, count: int = 1) -> bool:
        if self.item and self.item.id == item.id and item.stacked:
            if self.count + count > self.max_count:
                raise SlotOverloadError()
            self.count += count
            return True
        elif not self.item:
            if item.stacked and count > self.max_count:
                raise SlotOverloadError()
            self.item = item
            self.count = count
            return True
        else:
            loggers.inventory_logger.warning(f"Trying to add item with id {item.id} to slot [{self.slot_index}] which already has different item with id {self.item.id}")
            return False

    def get_item(self) -> tuple[Optional["Item"], int]:
        return (self.item, self.count)

    def clear_slot(self):
        self.item = None
        self.count = 0

    def interface(self) -> list[str] | None:
        if not self.item:
            return None
        return self.item.interface(count=self.count)

    def to_dict(self):
        return {
            "_": "Slot",
            "slot_index": self.slot_index,
            "item": self.item.to_dict() if self.item else None,
            "count": self.count
        }