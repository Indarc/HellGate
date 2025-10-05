from aiogram import Router
from server.bot.handlers import callback_handlers
from server.bot.handlers import command_handlers

def setup_routers() -> Router:
    router = Router(name="main")

    router.include_routers(
        callback_handlers.router,
        command_handlers.router
    )
    return router