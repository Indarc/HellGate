from aiogram import Router

from .interface import player
from game.classes.quests import guide_line

def setup_routers() -> Router:
    router = Router()

    router.include_routers(
        player.router,
        guide_line.router
    )
    return router