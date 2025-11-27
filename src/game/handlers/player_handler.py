from aiogram.types import Message, CallbackQuery

from server.loggers import Loggers
from game import user_manager
from game.classes.entity import Player
from game.classes.entity import User


async def load_user(message: Message | CallbackQuery, user: User):
    data = await user_manager.load_user(user.id)
    if not data:
        status = await user_manager.save_user(user)
        if not status:
            await message.answer("Извините произошла ошибка на стороне сервера. Попробуйте перезапустить игру /start")
            return