from aiogram import Router

from config import RESOURCES_DIR, user_db

from .manager import GameManager, UserManager, CombatManager, QuestManager, ItemManager


game_manager = GameManager(
    UserManager(user_db_executor=user_db),
    ItemManager(items_path=RESOURCES_DIR / "items"),
    CombatManager(),
    QuestManager()
)