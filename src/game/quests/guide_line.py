from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from game.classes.items.weapon import Weapon
from server.config import user_manager

from game.classes.entity.user_class import User
from game.handlers.state import State
from game.interface import PlayerInterface


router = Router(name="guide_line.router")

guide_lines: dict[str, "GuideLine"] = {

}

@router.callback_query(F.data == "start.guide")
async def start_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(State.guide)
    user = await user_manager.load_user(callback.from_user.id)
    guide_lines.setdefault(user.id, GuideLine(user, callback.message))
    await guide_lines[user.id].start()


class GuideLine:
    @router.callback_query(State.guide, F.data.contains("guide.progress"))
    async def guide_step(callback: CallbackQuery, state: FSMContext):
        data_list = callback.data.split('.')
        current_step = data_list[-1]
        guideline = guide_lines.get(callback.from_user.id)
        user = guideline.user
        if not guideline:
            # TODO error in logger
            return
        if current_step == "1":
            await guideline.open_item_guide()
        elif current_step == "2":
            await guideline.extra_item_info_guide()

    def __init__(self, user: User, message: Message):
        self.user = user
        self.message = message
        self.callback = "guide.progress"
        guide_lines.setdefault(user.id, self)
    
    async def start(self):
        # inventory guide
        guide_text = "Так выглядит ваш инвентарь, но вот загвостка у вас нету предметов(\nСейчас исправим!"
        text, markup = PlayerInterface.inventory(self.user.player)
        builder = InlineKeyboardBuilder.from_markup(markup)
        builder.row(InlineKeyboardButton(text="Продолжить", callback_data=f"{self.callback}.1"))
        await self.message.edit_text(text=guide_text, reply_markup=builder.as_markup())
    
    async def open_item_guide(self):
        weapon = Weapon(0)
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
    
    async def extra_item_info_guide(self):
        ...