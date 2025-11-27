# TODO обработчик команд в интерфейсе инвентаря
from aiogram import Router, F
from aiogram.types import CallbackQuery

from server.config import user_manager

router = Router(name="game.interface.handlers.inventory")


@router.callback_query(F.data.contains("inventory"))
async def entry(callback: CallbackQuery):
    user = await user_manager.load_user(callback.from_user.id)
    data_list = callback.data.split('.')
    data_list = data_list[1:]
    if data_list[0] == "open_slot":
        slot_index = int(data_list[1])
