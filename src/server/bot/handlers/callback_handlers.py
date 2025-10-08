from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from server.bot.handlers.catch import Catch
from server.resources.static_messages import CreateHero


router = Router(name="callback.handlers")


@router.callback_query(F.data == "create.hero")
async def create_hero(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Catch.nickname)
    text = CreateHero.nickname_create()
    await callback.message.edit_text(text=text)