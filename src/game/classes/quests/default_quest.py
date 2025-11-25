from game.classes.inventory.inventory import Inventory
from game.classes.items.item import Item
from server.loggers import Loggers

# from game.classes.entity import Player
from game.classes.inventory.error_class import DontEnoughSlotsError
from game.classes.items.item_import import items

from .errors import QuestAlreadyComplite
from . import get_clear_quests


class Quest:
    all_quests = get_clear_quests()
    def __init__(self, index: int=None, data: dict=None):
        if data:
            self.name = data.get("name")
            self.messages = data.get("messages")
            self.rewards = data.get("rewards")
            self.condition = data.get("condition")
            self.complite = data.get("complite")
        else:
            if index == None:
                Loggers.quest_logger.error("[QUEST_INIT] index parameter can`t be None")
                return
            self.quest_dict: dict = __class__.all_quests.get(index)
            if not self.quest_dict:
                Loggers.quest_logger.error(f"Can`t find quest with {index} index in all_quests")
                return
            
            if self.quest_dict.get("state"):
                return QuestAlreadyComplite()
            self.name = self.quest_dict.get("name")
            self.messages = self.quest_dict.get("messages")
            self.rewards = self.quest_dict.get("rewards")
            self.condition = self.quest_dict.get("condition")
            self.complite = self.quest_dict.get("complite")
    
    def check_condition(self) -> bool:
        if self.condition:
            return True
        else:
            return False
    
    def get_reward(self, player) -> bool | DontEnoughSlotsError:
        for reward in self.rewards:
            item_dict: dict = items.get(reward[0])
            count = reward[1]
            item_type = item_dict.get("_")
            Item_class: Item = Inventory.sorter.get(item_type)
            item = Item_class(id=item_dict.get("id"))

            for i in range(count):
                result = player.inventory.add_item(item)
                if isinstance(result, DontEnoughSlotsError):
                    return result
            return True

    def to_dict(self):
        return {
            "_": "quest",
            "name": self.name,
            "messages": self.messages,
            "rewards": self.rewards,
            "condition": self.condition,
            "complite": self.complite
        }