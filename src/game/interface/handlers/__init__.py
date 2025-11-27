from aiogram import Router
from .inventory import router as router1


router = Router(name="game.interface.handlers")

def setup_routers():
    router.include_routers(
        router1
    )
    return router