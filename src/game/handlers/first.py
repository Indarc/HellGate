from aiogram.types import Message, CallbackQuery

from server.config import Loggers
from game.classes.entity import Player
from game.classes.entity import User


async def check_user(message: Message | CallbackQuery, user: User):
    player = user.player