from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from game.classes.entity import User
from config import messages


def welcome_markup() -> tuple[InlineKeyboardMarkup, str]:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Создать персонажа", callback_data="create.hero")]
        ]
    )
    return (markup, messages.get("hello_message"))

def accept_nickname() -> tuple[InlineKeyboardMarkup, str]:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="save_nickname", style="success"),
             InlineKeyboardButton(text="✏️ Изменить", callback_data="change_nickname", style="primary")]
        ]
    )
    text = "Сохранить никнейм?"
    return (markup, text)

def start_quest(quest_index: int, user: User) -> tuple[InlineKeyboardMarkup, str]:
    # TODO
    # quest = game_manager.quest_manager
    text = f"Начать квест:\n{quest.name}"
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data=f"quest.start.{quest_index}", style="success"),
             InlineKeyboardButton(text="Отменить", callback_data=f"quest.abandon.{quest_index}", style="danger")]
        ]
    )
    # user.player.active_quest = user.player.quests[quest_index] # TODO попробовать переместить в инициализаю QuestRunner
    return (markup, text)