from aiogram.fsm.state import StatesGroup, State


class Catch(StatesGroup):
    nickname = State()