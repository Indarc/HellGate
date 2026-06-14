from config import RESOURCES_DIR, user_db, items_db

from .manager import GameManager, UserManager, CombatManager, QuestManager, ItemManager


game_manager = GameManager(
    UserManager(user_db_executor=user_db),
    ItemManager(items_db_executor=items_db),
    CombatManager(),
    QuestManager()
)