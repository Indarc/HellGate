from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from server.bot.handlers.catch import Catch
from config import setup_logger


router = Router(name="hero_creation.handler")
logger = setup_logger("hero_creation.logger")

def clear_string(text: str) -> str:
    text = text.strip().replace("\\", "").replace("/", "").replace(" ", "")
    return text

@router.message(Catch.nickname, F.text)
async def nickname_catch(message: Message, state: FSMContext):
    if not message.text or not state:
        logger.warning(f"Нет объекта Message или state\n Message: {message}\n State: {state}")
        return

    # update state data with user message to get dict with message
    await state.update_data(message=message.text)
    data: dict[str, str] = await state.get_data()
    await state.clear()
    
    user_input = data.get("message")
    user_input = clear_string(user_input)