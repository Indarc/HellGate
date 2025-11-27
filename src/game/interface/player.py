from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from game.classes.entity.player import Player


class PlayerInterface:
    def inventory(player: Player):
        inventory = player.inventory
        slots = inventory.slots
        builder = InlineKeyboardBuilder()
        for key, slot in slots.items():
            if slot.item is not None:
                item = slot.item
                count = slot.count
                builder.button(text=f"{item.name} x {count}", callback_data=f"inventory.open.slot.{key}")
            else:
                builder.button(text="Пусто", callback_data=f"inventory.open_slot.{key}")
        builder.adjust(4)
        text = "Инвентарь"
        return (text, builder.as_markup())
    
    def outfit(player: Player):
        ...
