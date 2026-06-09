from aiogram import Router

from bot.handlers import command_handlers
from bot.handlers import input_handlers
from bot.handlers import hero_creation_handlers




def setup_routers() -> Router:
    router = Router()

    router.include_routers(
        command_handlers.router,
        input_handlers.router,
        hero_creation_handlers.router
    )
    return router