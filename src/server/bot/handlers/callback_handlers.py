from aiogram import Router, F
from aiogram.types import Message


router = Router(name="callback.handlers")


@router.callback_query(F.data == "create.hero")
def create_hero(message: Message):
    ...