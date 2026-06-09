from tkinter.ttk import Style
from typing import TYPE_CHECKING, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


if TYPE_CHECKING:
    from game.classes.items import Item
    from game.classes.entity.player import Player


class PlayerInterface:
    @staticmethod
    def main(player: "Player") -> tuple[str, InlineKeyboardMarkup]:
        text = player.banner()
        markup = InlineKeyboardMarkup(inline_keyboard=
            [
                [InlineKeyboardButton(text="Экипировка", callback_data="equipment.open")]
            ]
        )
        return text, markup
    
    @staticmethod
    def inventory(player: "Player") -> tuple[str, InlineKeyboardMarkup]:
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
        builder.adjust(3)
        text = "Инвентарь"
        return (text, builder.as_markup())
    
    @staticmethod
    def equipment(player: "Player") -> tuple[str, InlineKeyboardMarkup]:
        callback = "equipment.open"
        text = f"""
----------------------Экипировка----------------------
Показатели:
Броня - {player.equipment.get_armor()}
Улонение - {player.equipment.get_evasion()}
...
"""
        slots = {
            "mainhand": "Оружие",
            "offhand": "Второстепеное оружие",
            "head": "Голова",
            "body": "Тело",
            "gloves": "Перчатки",
            "legs": "Ноги",
            "boots": "Обувь",
            "cloak": "Плащь",
            "amulet": "Амулет",
            "ring1": "Кольцо",
            "ring2": "Кольцо",
            "belt": "Пояс",
            "bag": "Сумка"
        }
        equipment_slots: dict[str, Optional["Item"]] = player.equipment.get_equipment()
        markup_builder = InlineKeyboardBuilder()
        for slot, item in equipment_slots.items():
            if slot and isinstance(slot, str):
                markup_builder.button(text=str(slots.get(slot)), callback_data=f"{callback}.{slot}", style="primary")
                item_name = item.name if item else "Пусто"
                if item:
                    markup_builder.button(text=item_name, callback_data=f"{callback}.{slot}", style="success")
                else:
                    markup_builder.button(text=item_name, callback_data=f"{callback}.{slot}")
        markup_builder.button(text="Закрыть", style="danger", callback_data=callback)
        markup_builder.adjust(2)

        return (text, markup_builder.as_markup())