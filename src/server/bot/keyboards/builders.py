from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import messages


def welcome_markup() -> tuple[InlineKeyboardMarkup, str]:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Создать персонажа", callback_data="create.hero")]
        ]
    )
    return (markup, messages.get("hello_message"))