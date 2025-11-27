from aiogram.fsm.state import StatesGroup
from aiogram.fsm.state import State as _State


class State(StatesGroup):
    quest = _State()
    guide = _State()