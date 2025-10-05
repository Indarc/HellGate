from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from server.resources.static_messages import *


def welcome_markup() -> tuple[InlineKeyboardMarkup, str]:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Создать персонажа", callback_data="create.hero")]
        ]
    )
    return (markup, welcome_message)