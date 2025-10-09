from .item import Item
from .logger import logger

from .errors import DontEnoughSpaceError


class Inventory:
    def __init__(self, max_space: int = 10):
        self.space = max_space
        self.max_space = max_space
        self.items: list[Item] = []
    
    def add_item(self, item: Item | list[Item]) -> None | DontEnoughSpaceError:
        if self.space - 1 == -1:
            return DontEnoughSpaceError()
        
        if isinstance(item, list) and len(item) > 0:
            self.items.append(item.pop())
            self.space -= 1
            if len(item) > 0:
                self.add_item(item)
        else:
            self.items.append(item)
    
    def remove_item(self, item_id: int) -> bool:
        try:
            item = self.items[item_id]
        except IndexError as error:
            logger.warning(f"IndexError with remove item from inventory: {error}")
            return False
        
        if item:
            self.items.pop(item_id)
    
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