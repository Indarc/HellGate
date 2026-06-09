from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from bot.keyboards.builders import accept_nickname
from bot.handlers.catch import Catch
from config import loggers

from game import game_manager
from game.classes.entity import Player
from game.classes.entity import User
from game.classes.quests.guide_line import GuideLine


router = Router(name="hero_creation.handler")

nicknames = {}

def clear_string(text: str) -> str:
    text = text.strip().replace("\\", "").replace("/", "").replace(" ", "")
    return text

@router.callback_query(F.data == "create.hero")
async def create_hero(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Catch.nickname)
    text = "Введите имя своего персонажа (вводите имя слитно по русский или английски):"
    await callback.message.edit_text(text=text)

@router.message(Catch.nickname, F.text)
async def nickname_catch(message: Message, state: FSMContext):
    if not message.text or not state:
        loggers.hero_creation_logger.warning(f"Нет объекта Message или state\n Message: {message}\n State: {state}")
        return

    # update state data with user message to get dict with message
    await state.update_data(message=message.text)
    data: dict[str, str] = await state.get_data()
    await state.clear()
    
    user_input= str(data.get("message"))
    user_input = clear_string(user_input)
    nicknames.update({message.chat.id: user_input})

    markup, text = accept_nickname()
    await message.answer(f"Ваш никнейм: {user_input}\n" + text, reply_markup=markup)


@router.callback_query(F.data == "save_nickname")
async def save_nickname(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    
    hero = Player(nicknames.pop(callback.from_user.id))
    user = User(callback.from_user.id, hero)

    await game_manager.user_manager.save_user(user)

    text = f"Теперь ты можешь пройти обучение, которое поможет тебе разобраться в механиках игры: инвентарь, экипировка, бой, классы и так далее.\nНе переживай, обучение не займет много времени, а после него ты сможешь свободно играть и наслаждаться процессом. Нажимай на кнопку ниже, чтобы начать обучение!"
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Начать", callback_data="start.guide", style="success"),
             InlineKeyboardButton(text="Пропустить", callback_data="start.game", style="primary")]
        ]
    )
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data == "change_nickname")
async def change_nickname(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Catch.nickname)
    text = "Введите имя своего персонажа (вводите имя слитно по русски или английски):"
    await callback.message.edit_text(text=text)
