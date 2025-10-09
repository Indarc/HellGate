from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from server.bot.handlers.catch import Catch


router = Router(name="callback.handlers")


@router.callback_query(F.data == "create.hero")
async def create_hero(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Catch.nickname)
    text = "Введите имя своего персонажа (вводите имя слитно по русский или английски):"
    await callback.message.edit_text(text=text)