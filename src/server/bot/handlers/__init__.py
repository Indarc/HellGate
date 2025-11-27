from aiogram import Router

from server.bot.handlers import callback_handlers
from server.bot.handlers import command_handlers
from server.bot.handlers import input_handlers
from server.bot.handlers import hero_creation_handlers

from game.quests import quester
from game.quests import guide_line
from game.interface import handlers


def setup_routers() -> Router:
    router = Router(name="main")

    router.include_routers(
        callback_handlers.router,
        command_handlers.router,
        input_handlers.router,
        hero_creation_handlers.router,
        quester.router,
        guide_line.router,
        handlers.setup_routers()
    )
    return router