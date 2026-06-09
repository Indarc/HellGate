from aiogram import Router, F
from aiogram.types import CallbackQuery

from game.interface import PlayerInterface


router = Router(name="interface.player.handler")


@router.callback_query(F.data.contains("equipment"))
async def equipment_handler(callback: CallbackQuery):
    from game import game_manager
    user = await game_manager.user_manager.load_user(callback.from_user.id)
    if not user:
        # TODO error
        return
    data_list = callback.data.split('.')
    action = data_list[1]
    if action == "open":
        text, markup = PlayerInterface.equipment(user.player)
        await callback.message.edit_text(text=text, reply_markup=markup)
    elif action == "equip":
        slot_index = int(data_list[2])
        user.player.equip_item(slot_id=slot_index)
        ...

@router.callback_query(F.data.contains("inventory"))
async def inventory_handler(callback: CallbackQuery):
    from game import game_manager
    from config import loggers
    user = await game_manager.user_manager.load_user(callback.from_user.id)
    if not user:
        # TODO error
        return
    data_list = callback.data.split('.')
    data_list = data_list[1:]
    if data_list[0] == "open_slot":
        slot_index = int(data_list[1])
        slot = user.player.inventory.get_slot(slot_id=slot_index)
        if not slot:
            return
        text_interface = slot.interface()
        if not callback.message:
            loggers.interface_logger.error(f"Can`t access to attribute message in callback: {callback}")
            return
        await callback.message.edit_text(text=text_interface)