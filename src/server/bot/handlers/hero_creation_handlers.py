from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from server.bot.handlers.catch import Catch
from server.classes.game.player import Player
from server.classes.game.user_class import User
from server.config import setup_logger
from server.config import user_db
from server.bot.handlers.command_handlers import start_command


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

    hero = Player(user_input)
    user = User(message.chat.id, hero)

    # add new user to database
    await user_db.add(user.id, user)

    await start_command(message)