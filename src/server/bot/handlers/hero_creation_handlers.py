from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from server.config import user_manager
from server.bot.keyboards.builders import accept_nickname
from server.bot.handlers.catch import Catch
from server.loggers import Loggers

from game.classes.entity import Player
from game.classes.entity import User
from game.quests.guide_line import GuideLine


router = Router(name="hero_creation.handler")

nicknames = {}

def clear_string(text: str) -> str:
    text = text.strip().replace("\\", "").replace("/", "").replace(" ", "")
    return text

@router.message(Catch.nickname, F.text)
async def nickname_catch(message: Message, state: FSMContext):
    if not message.text or not state:
        Loggers.hero_creation_logger.warning(f"Нет объекта Message или state\n Message: {message}\n State: {state}")
        return

    # update state data with user message to get dict with message
    await state.update_data(message=message.text)
    data: dict[str, str] = await state.get_data()
    await state.clear()
    
    user_input = data.get("message")
    user_input = clear_string(user_input)
    nicknames.setdefault(message.chat.id, user_input)

    markup, text = accept_nickname()
    await message.answer(f"Ваш никнейм: {user_input}\n" + text, reply_markup=markup)


@router.callback_query(F.data == "save_nickname")
async def save_nickname(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    
    hero = Player(nicknames.pop(callback.message.chat.id))
    user = User(callback.from_user.id, hero)

    await user_manager.save_user(user)

    text = f"Теперь тебе надо пройти гайд лайн, который поможет разобраться в механиках игры (инвентарь, экипировка, бой и т.п.)"
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Начать", callback_data="start.guide")]
        ]
    )
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data == "change_nickname")
async def change_nickname(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Catch.nickname)
    text = "Введите имя своего персонажа (вводите имя слитно по русски или английски):"
    await callback.message.edit_text(text=text)
