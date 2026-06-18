from config import user_db, items_db, entity_db, loggers

from .manager import GameManager, UserManager, CombatManager, QuestManager, ItemManager, EntityManager


game_manager = GameManager(
    user_manager=UserManager(user_db_executor=user_db, logger=loggers.user_manager_logger),
    item_manager=ItemManager(items_db_executor=items_db, logger=loggers.item_manager_logger),
    entity_manager=EntityManager(entity_db_executor=entity_db, logger=loggers.entity_manager_logger),
    combat_manager=CombatManager(),
    quest_manager=QuestManager()
)