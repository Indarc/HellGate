from types import NoneType

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.keyboards.builders import welcome_markup, start_quest
from config import user_db, loggers

from game import game_manager
from game.classes.entity import User


router = Router(name="command.handler")

@router.message(CommandStart())
async def start_command(message: Message):
    if not message.from_user:
        loggers.bot_handlers.warning(f"Message object has not [from_user] object. {message}")
        return None
    if not message.from_user.id:
        loggers.bot_handlers.warning(f"[from_user] object has not [id] variable. {message.from_user}")
        return None
    data = await game_manager.user_manager.load_user(message.from_user.id)
    if not data:
        markup, text = welcome_markup()
        await message.answer(text=text, reply_markup=markup)
    else:
        # TODO handle user end load his last location and actions
        pass
