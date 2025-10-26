from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from server.bot.keyboards.builders import welcome_markup
from server.config import user_db


router = Router(name="command.handler")

@router.message(CommandStart())
async def start_command(message: Message):
    user_id = message.chat.id
    data = await user_db.get(user_id)
    if not data:
        markup, text = welcome_markup()
        await message.answer(text=text, reply_markup=markup)
    else:
        ...
