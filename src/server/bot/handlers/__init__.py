from aiogram import Router
from server.bot.handlers import callback_handlers
from server.bot.handlers import command_handlers
from server.bot.handlers import input_handlers
from server.bot.handlers import hero_creation_handlers

def setup_routers() -> Router:
    router = Router(name="main")

    router.include_routers(
        callback_handlers.router,
        command_handlers.router,
        input_handlers.router,
        hero_creation_handlers.router
    )
    return router