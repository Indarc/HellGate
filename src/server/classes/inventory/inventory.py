from .item import Item
from .logger import logger

from .error_class import DontEnoughSpaceError, ItemRemoveError


class Inventory:
    def __init__(self, max_space: int = 10):
        self.space = max_space
        self.max_space = max_space
        self.items: dict[int, Slot] = {x : Slot() for x in range(0, max_space)}
    
    def add_item(self, item: Item) -> None | DontEnoughSpaceError:
        if self.space - 1 == -1:
            return DontEnoughSpaceError()
        
        for i, slot in self.items.items(): # check if item in inventory and add 1 count
            if slot.item == item:
                self.items[i].count += 1
                if not slot.item.stacked:
                    self.space -= 1
                return
        
        for i, slot in self.items.items(): # if item not in inventory then claim empty slot in inventory
            if not slot.item:
                self.items[i].item = item
                self.items[i].count = 1
                self.space -= 1
                return
    
    def add_items(self, items: list[Item]) -> None | DontEnoughSpaceError:   
        stored = []
        for item in items: #
            for i, slot in self.items.items(): # try find sample item in inventory and add count
                if slot.item == item and item not in stored:
                    item_count = items.count(item)
                    if not item.stacked:
                        if self.space - item_count < 0:
                            return DontEnoughSpaceError(f"Не хватает места в инвентаре. Свободно: {self.space}, требуется: {item_count}")
                        self.space -= item_count
                    self.items[i].count += item_count
                    stored.append(item)
                    break
            
            if item not in stored: # if item not in inventory, take empty slot
                for i, slot in self.items.items():
                    if not slot.item:
                        item_count = items.count(slot.item)
                        if not item.stacked:
                            if self.space - item_count < 0:
                                return DontEnoughSpaceError(f"Не хватает места в инвентаре. Свободно: {self.space}, требуется: {item_count}")
                            self.space -= item_count
                        else:
                            self.space -= 1
                        self.items[i].item = item
                        self.items[i].count = item_count
                        stored.append(item)
                        
    
    def remove_item(self, slot_id: int, count: int=1) -> None | ItemRemoveError:
        item = self.items.get(slot_id)
        if not item:
            logger.warning(f"Item in slot [{slot_id}] is [None]")
            return ItemRemoveError(message="Предмет, который Вы пытаетесь удалить, не существует.")
        
        if count > 1:
            slot = self.items.get(slot_id)
            item = slot.get("item")
            count = slot.get("count")
    
    def items_count(self) -> list[list[Item, int]]:
        counter: list[list[Item, int]] = []
        counted = []
        counting = None
        for item in self.items:
            counting = item
            count = 0
            for counting_item in self.items:
                if counting_item == counting:
                    count += 1
            counted.append(counting)
            counter.append([counting, count])
        
        return counter


class Slot:
    def __init__(self, item: Item=None, count: int=0):
        self.item = item
        self.count = count