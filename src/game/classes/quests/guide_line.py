from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asyncpg import FatalPostgresError

if TYPE_CHECKING:
    from game.classes.entity.player import Player
from game.classes.inventory import Slot
from config import loggers


from game.classes.entity.user_class import User
from game.handlers.state import State
from game.interface import PlayerInterface


separator = "\n----------------------------------\n"

guide_lines: dict[str, "GuideLine"] = {

}

router = Router(name="game.guide_line.handler")

@router.callback_query(F.data == "start.guide")
async def start_callback(callback: CallbackQuery, state: FSMContext):
    from game import game_manager
    user: User | None = await game_manager.user_manager.load_user(callback.from_user.id)
    if not user:
        loggers.quest_logger.error(f"User not found: {callback.from_user.id}")
        return
    if isinstance(callback.message, Message):
        await state.set_state(State.guide)
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
        await guideline.equipment_guide(user.player.inventory.slots[0])
    elif current_step == "4":
        await guideline.weapon_equip_guide(user.player)
    elif current_step == "5":
        await guideline.equipment_interface_guide(user.player)
    elif current_step == "6":
        await guideline.guideline_end(user.player)
    elif current_step == "end":
        await state.clear()
        guide_lines.pop(str(callback.from_user.id))
    else:
        loggers.quest_logger.warning(f"Uncorrect guide line step: {current_step}")
        return


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
        builder.row(InlineKeyboardButton(text="Продолжить", callback_data=self.callback + ".1", style="primary"))
        await self.message.edit_text(text=guide_text, reply_markup=builder.as_markup())
    
    async def open_item_guide(self):
        from game import game_manager
        weapon = await game_manager.item_manager.get("rusty_sword")
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
                    callback_data=self.callback + ".2",
                    style="primary"
                )
            else:
                new_builder.button(
                    text=button.text,
                    callback_data="None"
                )
        new_builder.adjust(3)
        await self.message.edit_text(text=guidetext, reply_markup=new_builder.as_markup())
    
    async def extra_item_info_guide(self, slot: Slot):
        info = slot.interface()
        if not info:
            return
        text = separator.join(info)
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Продолжить", callback_data=self.callback + ".3", style="primary")]
            ]
        )
        await self.message.edit_text(text=text, reply_markup=markup)
    
    async def equipment_guide(self, slot: Slot):
        info = slot.interface()
        if not info:
            return
        
        text = 'Теперь расскажем вам, как надеть экипировку на вашего персонажа.\nВ описании предмeта появилась кнопка "Экипировать". Нажмите на неё.'
        text = text + "\n\n" + separator.join(info)
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Экипировать", callback_data=self.callback + ".4", style="success")]
            ]
        )
        await self.message.edit_text(text=text, reply_markup=markup)

    async def weapon_equip_guide(self, player: "Player"):
        player.equip_item(slot_id=0)
        text, markup = PlayerInterface.main(player)
        new_markup = self.change_markup(markup, callback_state=self.callback + ".5")
        await self.message.edit_text(text=text, reply_markup=new_markup)

    async def equipment_interface_guide(self, player: "Player"):
        text, markup = PlayerInterface.equipment(player)
        text = """
Это ваша экипировка. Чтобы заменить или снять предмет нужно на него нажать далее снять или заменить.
Нажмите на любую кнопку, чтобы продолжить.
"""
        new_markup = self.change_markup(markup, callback_state=self.callback + ".6")
        await self.message.edit_text(text=text, reply_markup=new_markup)

    async def guideline_end(self, player: "Player"):
        text = """
Обучение закончено!
Теперь можете начать исследовать мир.
"""
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Продолжить", style="primary", callback_data=self.callback + ".end")]
            ]
        )
        await self.message.edit_text(text=text, reply_markup=markup)

    def change_markup(self, markup: InlineKeyboardMarkup, callback_state: str) -> InlineKeyboardMarkup:
        new_inline_keyboard = []
        for row in markup.inline_keyboard:
            new_row = []
            for button in row:
                if button.model_extra:
                    button_style = button.model_extra.get("style")
                    new_row.append(InlineKeyboardButton(
                                    text=button.text,
                                    callback_data=callback_state,  # или какой-то другой callback
                                    style=button_style
                                ))
                else:
                    new_row.append(InlineKeyboardButton(
                                    text=button.text,
                                    callback_data=callback_state,  # или какой-то другой callback
                                ))
            new_inline_keyboard.append(new_row)
        return InlineKeyboardMarkup(inline_keyboard=new_inline_keyboard)