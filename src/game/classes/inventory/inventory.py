from game.classes.items import Weapon
from game.classes.items import Item
from game.classes.items import Armor
from game.classes.items import Jewelry
from server.loggers import Loggers

from .error_class import ItemRemoveError, DontEnoughSlotsError


class Inventory:
    sorter = {
        "another": Item,
        "weapon": Weapon,
        "armor": Armor,
        "jewelry": Jewelry
    }
    def __init__(self, max_space: int = 10, data: dict=None):
        if data:
            self.space = data.get("space")
            self.max_space = data.get("max_space")
            self.slots: dict[int, Slot] = {}
            slots_dict: dict = data.get("slots")
            for slot_id, slot_dict in slots_dict.items():
                self.slots.setdefault(slot_id, Slot(data=slot_dict))
        else:
            self.space = max_space
            self.max_space = max_space
            self.slots: dict[int, Slot] = {x : Slot() for x in range(0, max_space)}
    
    def add_item(self, item: Item) -> None | DontEnoughSlotsError:
        if self.space == 0:
            return DontEnoughSlotsError()
        
        for i, slot in self.slots.items(): # check if item in inventory and add 1 count
            if slot.item == item:
                self.slots[i].count += 1
                if not slot.item.stacked:
                    self.space -= 1
                return
        
        for i, slot in self.slots.items(): # if item not in inventory then claim empty slot in inventory
            if not slot.item:
                self.slots[i].item = item
                self.slots[i].count = 1
                self.space -= 1
                return
    
    def add_items(self, items: list[Item]) -> None | DontEnoughSlotsError:   
        stored = []
        for item in items: #
            for i, slot in self.slots.items(): # try find sample item in inventory and add count
                if slot.item == item and item not in stored:
                    item_count = items.count(item)
                    if not item.stacked:
                        if self.space - item_count < 0:
                            return DontEnoughSlotsError(f"Не хватает места в инвентаре. Свободно: {self.space}, требуется: {item_count}")
                        self.space -= item_count
                    self.slots[i].count += item_count
                    stored.append(item)
                    break
            
            if item not in stored: # if item not in inventory, take empty slot
                for i, slot in self.slots.items():
                    if not slot.item:
                        item_count = items.count(slot.item)
                        if not item.stacked:
                            if self.space - item_count < 0:
                                return DontEnoughSlotsError(f"Не хватает места в инвентаре. Свободно: {self.space}, требуется: {item_count}")
                            self.space -= item_count
                        else:
                            self.space -= 1
                        self.slots[i].item = item
                        self.slots[i].count = item_count
                        stored.append(item)
        # TODO update user in db
                        
    def remove_item(self, slot_id: int, count: int=1) -> None | ItemRemoveError:
        item = self.slots.get(slot_id)
        if not item:
            Loggers.inventory_logger.warning(f"Item in slot [{slot_id}] is [None]")
            return ItemRemoveError(message="Предмет, который Вы пытаетесь удалить, не существует.")
        
        if count >= 1:
            slot = self.slots.get(slot_id)
            item = slot.item
            count = slot.count
            if count > slot.count:
                count = slot.count
            elif count == slot.count:
                self.slots[slot_id].item = None
                self.slots[slot_id].count = 0
            else:
                self.slots[slot_id].count -= count
        elif count <= 0:
            return ItemRemoveError(message="Неверное колличество для удаления предмета")

        # TODO update user in db
    
    # ?????????????? нахуя написал
    def get_items(self) -> list[list[int, Item, int]]:
        items = []
        for i, slot in self.slots.items():
            items.append([i ,slot.item, slot.count])
        
        return items

    def to_dict(self) -> dict:
        slots = {}
        for i, slot in self.slots.items():
            if slot.item is None:
                slots.setdefault(i, {"item": None, "count": 0})
                continue
            slots.setdefault(i, {"item": slot.item.to_dict(), "count": slot.count})
        inv_dict = {
            "max_space": self.max_space,
            "space": self.space,
            "slots": slots
        }
        return inv_dict

class Slot:
    def __init__(self, item: Item=None, count: int=0, data: dict=None):
        if data:
            item: dict = data.get("item")
            if item:
                item_type = item.get("_")
                if item_type == "weapon":
                    self.item = Weapon(data=item)
                elif item_type == "armor":
                    self.item = None
                elif item_type == "jewelry":
                    self.item = None
                elif item_type == "another":
                    self.item = Item(data=data)
                else:
                    self.item = None
            else:
                self.item = None
            self.count = data.get("count")
            pass
        else:
            self.item = item
            self.count = count
    
    def to_dict(self):
        return {
            "_": self.item.item_dict.get("_"),
            "item": self.item.to_dict() if self.item else None,
            "count": self.count
        }