from aiogram import Router, F
from aiogram.types import CallbackQuery

from server.config import game_manager


router = Router(name="game.interface.outfit.router")


@router.callback_query(F.data.contains("outfit"))
async def entry(callback: CallbackQuery):
    user = await game_manager.user_manager.load_user(callback.from_user.id)
    data_list = callback.data.split('.')
    action = data_list[1]
    if action == "equip":
        slot_index = int(data_list[2])
        item_to_equip = user.player.inventory.slots[slot_index]
        user.player.outfit.equip(item_to_equip)