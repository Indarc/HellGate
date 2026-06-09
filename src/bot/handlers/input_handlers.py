from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.handlers.catch import Catch

router = Router(name="input.handler")
