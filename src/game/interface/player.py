from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from game.classes.entity.player import Player


class PlayerInterface:
    @staticmethod
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
    
    @staticmethod
    def outfit(player: Player):
        outfit = player.outfit
        text = f"""
Экипировка
--------------
Оружие: {outfit.main_weapon.name if outfit.main_weapon else "Пусто"}
Второстепеное оружие: {outfit.offhand_weapon.name if outfit.offhand_weapon else "Пусто"}
Голова: {outfit.helmet.name if outfit.helmet else "Пусто"}
Тело: {outfit.armor.name if outfit.armor else "Пусто"}
Ноги: {outfit.legs.name if outfit.legs else "Пусто"}
Перчатки: {outfit.gloves.name if outfit.gloves else "Пусто"}
Обувь: {outfit.boots.name if outfit.boots else "Пусто"}
Амулет: {outfit.amulet.name if outfit.amulet else "Пусто"}
Кольцо: {outfit.ring1.name if outfit.ring1 else "Пусто"}
Кольцо: {outfit.ring2.name if outfit.ring2 else "Пусто"}
Пояс: {outfit.belt.name if outfit.belt else "Пусто"}
Сумка: {outfit.bag.name if outfit.bag else "Пусто"}
"""
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="")] # TODO add outfit management buttons
            ]
        )
