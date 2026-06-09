import asyncio
import sys

from aiogram import Router

from config import bot, dp, init_db, shutdown, loggers
from bot.handlers import setup_routers as setup_bot_routers
from game.handlers import setup_routers as setup_game_routers

main_router = Router(name="main")
main_router.include_routers(
    setup_bot_routers(),
    setup_game_routers()
)

dp.include_router(main_router)

async def main():
    conn = await init_db()
    if isinstance(conn, Exception):
        sys.exit(1)
    
    try:
        loggers.main.info("Bot started")
        await dp.start_polling(bot)
    except Exception as e:
        loggers.config.error(f"Unexpected error: {e}")
    finally:
        loggers.config.info("Starting shutdown process...")
        await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        loggers.main.info("Stopped from keyboard")