from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from server.bot.keyboards.builders import welcome_markup
from server.config import user_db
from server.classes.game.user_class import User
from server.classes.game.player import Player
from server.bot.game_handlers.first import check_user

router = Router(name="command.handler")

@router.message(CommandStart())
async def start_command(message: Message):
    user_id = message.chat.id
    data: User = await user_db.get(user_id)
    if not data:
        markup, text = welcome_markup()
        await message.answer(text=text, reply_markup=markup)
    else:
        text = data.player.banner()
        await message.answer(text=text)
