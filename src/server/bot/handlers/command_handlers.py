from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from server.bot.keyboards.builders import welcome_markup


router = Router(name="command.handler")

@router.message(CommandStart())
async def start_command(message: Message):
    markup, text = welcome_markup()
    await message.answer(text=text, reply_markup=markup)