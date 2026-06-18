from game.classes.inventory.error_class import DontEnoughSlotsError, SlotOverloadError
from game.classes.items.item import Item
from .item_manager import ItemManager
from .user_manager import UserManager
from .combat_manager import CombatManager
from .quest_manager import QuestManager
from .entity_manager import EntityManager
from config import loggers


class GameManager:
    """Class for managing game state and interactions"""
    def __init__(self, user_manager: UserManager, item_manager: ItemManager, entity_manager: EntityManager, combat_manager: CombatManager, quest_manager: QuestManager):
        self.user_manager: UserManager = user_manager
        self.item_manager: ItemManager = item_manager
        self.combat_manager = combat_manager
        self.quest_manager = quest_manager
        self.entity_manager = entity_manager
    
    def get_user(self, user_id: int):
        return self.user_manager.load_user(user_id)
    
    async def get_item(self, item_identificator: str) -> Item | None:
        return await self.item_manager.get(item_identificator)


    
    async def give_item_to_player(self, user_id: int, item_identificator: str) -> bool:
        user = await self.get_user(user_id)
        if not user:
            return False
        item = await self.get_item(item_identificator)
        if not item:
            loggers.game.error(f"Item with ID {item_identificator} not found.")
            return False
        try:
            user.player.inventory.add_item(item)
        except DontEnoughSlotsError:
            loggers.game.warning(f"Player {user_id} has not enough slots in inventory.")
            return False
        except SlotOverloadError:
            loggers.game.warning(f"Player {user_id} has not enough space in slot.")
            # TODO send message about that to user
            return False
        return True

    async def spawn_user(self, location_id: int):
        ...