from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from server.bot.keyboards.builders import welcome_markup, start_quest
from server.config import user_db, user_manager
from game.classes.entity import User


router = Router(name="command.handler")

@router.message(CommandStart())
async def start_command(message: Message):
    # data: User = await user_db.get(user_id)
    data = await user_manager.load_user(message.chat.id)
    if not data:
        markup, text = welcome_markup()
        await message.answer(text=text, reply_markup=markup)
    else:
        # TODO handle user end load his last location and actions
        pass
