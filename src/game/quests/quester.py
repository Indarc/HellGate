from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from game.classes.inventory.inventory import Inventory
from game.classes.items.item import Item
from game.classes.quests.default_quest import Quest
from game.classes.entity import User
from game.classes.entity import Player
from game.handlers.state import State

from server.config import user_manager
from server.loggers import Loggers

from game.classes.quests.errors import QuestAlreadyComplite
from game.classes.items.item_import import items


router = Router(name="quests.router")

users_quests_runners = {

}

@router.callback_query(F.data == "quest.start")
async def start_quest_callback(callback: CallbackQuery, state: FSMContext):
    user: User = await user_manager.load_user(callback.message.chat.id)
    if user.player.active_quest.complite:
        await callback.message.edit_text(text=f'Квест "{user.player.active_quest.name}" уже выполнен.')
        user.player.active_quest = None
        return
    await state.set_state(State.quest)
    quest_runner = QuestRunner(callback.message, user)
    users_quests_runners.setdefault(user.id, quest_runner)
    await quest_runner.start()

@router.callback_query(F.data == "quest.abandon")
async def abandon_quest(callback: CallbackQuery, state: FSMContext):
    user = await user_manager.load_user(callback.message.chat.id)
    # TODO

class QuestRunner:
    @router.callback_query(State.quest, F.data)
    async def action(callback: CallbackQuery, state: FSMContext):
        data_list = callback.data.split('.')
        quest_runner: QuestRunner = users_quests_runners[callback.message.chat.id]
        quest = quest_runner.quest
        if quest.callback != data_list[0] + '.' + data_list[1]:
            Loggers.quest_logger.warning(f"Quest data in Callback not equal data in quest callback variable\n Callback: {callback.data}\nQuest.callback: {quest.callback}")
            return
        user_choice = callback.data.split('.')[-1]
        last_action = callback.data.split('.')[-2]
        if last_action in quest_runner.quest.conditions:
            quest_runner.quest.complite = True
            result = quest_runner.quest.get_reward(quest_runner.user.player)
            await state.clear()
            await quest_runner.end()
            return

        def get_current_step(messages: dict, user_actions: list, i=0) -> dict:
            act = messages.get(user_actions[i])
            i += 1
            if len(user_actions) == i:
                return act
            return get_current_step(act, user_actions, i)
                
        current_step = get_current_step(messages=quest_runner.quest.messages, user_actions=quest_runner.actions)
        next_step: dict = current_step.get(user_choice)
        actions: dict = next_step.get("actions")
        text = next_step.get("message")
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=act.get("text"), callback_data=f"{quest_runner.quest.callback}.{act.get('callback')}.{act.get('action')}") for act in actions]
            ]
        )
        quest_runner.actions.append(user_choice)
        await callback.message.edit_text(text=text, reply_markup=markup)
    
    def __init__(self, message: Message, user: User):
        # TODO update player active quest
        self.user = user
        self.message = message
        self.quest: Quest = user.player.active_quest
        self.actions = []

    async def start(self):
        _start: dict = self.quest.messages.get("start")
        message = _start.get("message")
        actions: dict = _start.get("actions")
        self.actions.append("start")
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=action.get("text"), callback_data=f"{self.quest.callback}.{action.get('callback')}.{action.get('action')}") for action in actions]
            ]
        )
        await self.message.edit_text(text=message, reply_markup=markup)

    async def end(self) -> str:
        self.user.player.active_quest = None
        users_quests_runners.pop(self.user.id)
        rewards: list[Item, int] = []
        for reward in self.quest.rewards:
            item_index = reward[0]
            item_count = reward[1]
            item_dict: dict = items.get(item_index)
            item = Inventory.sorter.get(item_dict.get("_"))(item_index)
            rewards.append((item, item_count))
        rewards_texts = ""
        for reward in rewards:
            item: Item = reward[0]
            count: int = reward[1]
            rewards_texts += f"{item.name} x{count}\n"
        text = f'''
        Вы успешно выполнили квест "{self.quest.name}".
        Получены награды:
        {rewards_texts}
        '''
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Продолжить", callback_data="last_location")]
            ]
        )
        await self.message.edit_text(text=text, reply_markup=markup)
        del(self)