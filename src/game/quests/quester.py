from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from game.classes.inventory.inventory import Inventory
from game.classes.items.item import Item
from game.classes.quests.default_quest import Quest
from game.classes.entity import User
from game.classes.entity import Player
from game.handlers.state import State

from server.config import user_db
from server.loggers import Loggers

from game.classes.quests.errors import QuestAlreadyComplite
from game.classes.items.item_import import items


router = Router(name="quests.router")

users_quests = {

}

@router.callback_query(F.data == "quest.start.0")
async def start_quest(callback: CallbackQuery, state: FSMContext):
    await state.set_state(State.quest)
    quest_index = int(callback.data.split(".")[-1])
    user = await user_db.get(callback.message.chat.id)
    quest_runner = QuestRunner(callback.message, user, quest_index)
    users_quests.setdefault(user.id, quest_runner)
    await quest_runner.start()

class QuestRunner:
    @router.callback_query(State.quest, F.data)
    async def action(callback: CallbackQuery, state: FSMContext):
        quest_runner: QuestRunner = users_quests[callback.message.chat.id]
        if callback.data == quest_runner.quest.condition:
            quest_runner.quest.complite = True
            result = quest_runner.quest.get_reward(quest_runner.user.player)
            print(result)

    
    def __init__(self, message: Message, user: User, index: int):
        self.user = user
        self.message = message
        self.quest: Quest = user.player.quests[index]
        if self.quest.complite:
            return QuestAlreadyComplite()
        self.progres = 0

    async def start(self):
        message, actions = self.quest.messages[0]
        self.progres += 1
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=action[0], callback_data=action[1]) for action in actions]
            ]
        )
        await self.message.edit_text(text=message, reply_markup=markup)

    async def complited(self) -> str:
        rewards: list[Item, int] = []
        for reward in self.quest.rewards:
            item_index = reward[0]
            item_count = reward[1]
            item_dict: dict = items.get(item_index)
            item = Inventory.sorter(item_dict.get("_"))(item_index)
            rewards.append(item, item_count)
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