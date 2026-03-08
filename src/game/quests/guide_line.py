from typing import Optional

from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from game.classes.entity.player import Player
from game.classes.inventory import Inventory, Slot
from game.classes.items import Weapon
from server.config import game_manager, loggers


from game.classes.entity.user_class import User
from game.handlers.state import State
from game.interface.handlers.inventory import weapon_desc
from game.interface import PlayerInterface


router = Router(name="guide_line.router")

guide_lines: dict[str, "GuideLine"] = {

}

@router.callback_query(F.data == "start.guide")
async def start_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(State.guide)
    user: User | None = await game_manager.user_manager.load_user(callback.from_user.id)
    if not user:
        loggers.quest_logger.error(f"User not found: {callback.from_user.id}")
        return
    if isinstance(callback.message, Message):
        guide_lines.setdefault(str(user.id), GuideLine(user, callback.message))
        await guide_lines[str(user.id)].start()
    else:
        loggers.quest_logger.error(f"Message not found in callback: {callback.from_user.id}")


@router.callback_query(State.guide, F.data.contains("guide.progress"))
async def guide_step(callback: CallbackQuery, state: FSMContext):
    if not callback.data:
        loggers.quest_logger.error(f"Callback data is missing for user {callback.from_user.id}")
        return
    data_list = callback.data.split('.')
    current_step = data_list[-1]
    guideline = guide_lines.get(str(callback.from_user.id))
    if not guideline:
        loggers.quest_logger.error(f"GuideLine not found for user {callback.from_user.id}")
        return
    user = guideline.user
    if not guideline:
        loggers.quest_logger.error(f"GuideLine not found for user {callback.from_user.id}")
        return
    if current_step == "1":
        await guideline.open_item_guide()
    elif current_step == "2":
        await guideline.extra_item_info_guide(user.player.inventory.slots[0])
    elif current_step == "3":
        await guideline.outfit_guide(user.player.inventory.slots[0])
    elif current_step == "4":
        await guideline.weapon_equip_guide(user.player)


class GuideLine:
    def __init__(self, user: User, message: Message):
        self.user = user
        self.message = message
        self.callback = "guide.progress"
        guide_lines.setdefault(str(self.user.id), self)
    
    async def start(self):
        # inventory guide
        guide_text = "Так выглядит ваш инвентарь, но вот проблема у вас нету предметов(\nСейчас исправим!"
        text, markup = PlayerInterface.inventory(self.user.player)
        builder = InlineKeyboardBuilder.from_markup(markup)
        builder.row(InlineKeyboardButton(text="Продолжить", callback_data=f"{self.callback}.1"))
        await self.message.edit_text(text=guide_text, reply_markup=builder.as_markup())
    
    async def open_item_guide(self):
        weapon = game_manager.item_manager.get_item(0)
        if not weapon:
            loggers.quest_logger.error(f"Weapon with ID 0 not found for guide line.")
            return
        self.user.player.inventory.add_item(weapon)
        guidetext = "Вы получили своё первое оружие. Смотрите как изменился ваш инвентарь.\nТеперь нажмите на него, чтобы открыть подробное описание"
        text, markup = PlayerInterface.inventory(self.user.player)
        builder = InlineKeyboardBuilder.from_markup(markup)
        new_builder = InlineKeyboardBuilder()
        for i, button in enumerate(builder.buttons):
            if i == 0:
                new_builder.button(
                    text=button.text,
                    callback_data=f"{self.callback}.2"
                )
            else:
                new_builder.button(
                    text=button.text,
                    callback_data="None"
                )
        new_builder.adjust(4)
        await self.message.edit_text(text=guidetext, reply_markup=new_builder.as_markup())
    
    async def extra_item_info_guide(self, slot: Slot):
        text = weapon_desc(slot)
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Продолжить", callback_data=f"{self.callback}.3", style="primary")]
            ]
        )
        await self.message.edit_text(text=text, reply_markup=markup)
    
    async def outfit_guide(self, slot: Slot):
        text = 'Теперь расскажем вам, как надеть экипировку на вашего персонажа.\nВ описании предмeта появилась кнопка "Экипировать". Нажмите на неё.'
        text = text + "\n\n" + weapon_desc(slot)
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Экипировать", callback_data=f"{self.callback}.4", style="success")]
            ]
        )
        await self.message.edit_text(text=text, reply_markup=markup)

    async def weapon_equip_guide(self, player: Player):
        player.outfit.equip(player.inventory.slots[0].item)

    async def battle_guide(self):
        ...