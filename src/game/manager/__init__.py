from .combat_manager import CombatManager
from .game_manager import GameManager
from .item_manager import ItemManager
from .quest_manager import QuestManager
from .user_manager import UserManager
from .entity_manager import EntityManager


__all__ = ["CombatManager", "GameManager", "ItemManager", "QuestManager", "UserManager", "AttackResult", "EntityManager"]


class AttackResult:
    def __init__(self, alive: bool=True, damage: float=0.0, evaded: bool=False, crit: bool=False):
        self.alive = alive
        self.damage = damage
        self.evaded = evaded
        self.crit = crit