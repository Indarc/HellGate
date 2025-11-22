from aiogram.types import Message

from server.bot.game_handlers.logger import logger
from server.classes.game.player import Player
from server.classes.game.user_class import User

async def check_user(message: Message, user_data: dict):
    t = user_data.get("_")
    if t != "User":
        logger.error(f"Invalid data from user_data: {user_data}")
    
    user = User(data=user_data)