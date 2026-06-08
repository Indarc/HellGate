from aiogram import Router
from .inventory import router as inventory_router
from .outfit import router as outfit_router


router = Router(name="game.interface.handlers")

def setup_routers():
    router.include_routers(
        inventory_router,
        outfit_router
    )
    return router