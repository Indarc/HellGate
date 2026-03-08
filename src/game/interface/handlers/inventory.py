# TODO обработчик команд в интерфейсе инвентаря
from aiogram import Router, F
from aiogram.types import CallbackQuery

from game.classes.entity import Player
from game.classes.inventory.inventory import Slot
from game.classes.items import Weapon, Armor, Jewelry, Item
from server.config import game_manager
from server.config import loggers

router = Router(name="game.interface.handlers.inventory")


@router.callback_query(F.data.contains("inventory"))
async def entry(callback: CallbackQuery):
    user = await game_manager.user_manager.load_user(callback.from_user.id)
    data_list = callback.data.split('.')
    data_list = data_list[1:]
    if data_list[0] == "open_slot":
        slot_index = int(data_list[1])
        inventory = user.player.inventory
        slot = inventory.slots[slot]
        if not slot.item:
            return
        if isinstance(slot.item, Weapon):
            weapon_desc(slot)
        elif isinstance(slot.item, Armor):
            ...
        elif isinstance(slot.item, Jewelry):
            ...
        elif isinstance(slot.item, Item):
            ...
        else:
            ...

def weapon_desc(slot: Slot) -> str:
    item = slot.item
    count = slot.count
    desc = item.banner(count)
    return desc
