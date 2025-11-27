from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from server.config import user_db, user_manager
from server.bot.keyboards.builders import accept_nickname, start_quest
from server.bot.handlers.catch import Catch
from server.loggers import Loggers

from game.classes.entity import Player
from game.classes.entity import User


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
    user = User(callback.message.chat.id, hero)

    # add new user to database
    await user_manager.save_user(user)

    markup, text = start_quest(0, user)
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data == "change_nickname")
async def save_nickname(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Catch.nickname)
    text = "Введите имя своего персонажа (вводите имя слитно по русский или английски):"
    await callback.message.edit_text(text=text)
