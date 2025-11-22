import asyncio
import sys

from server.config import bot, dp, setup_logger, init_db, shutdown
from server.bot.handlers import setup_routers


dp.include_router(setup_routers())

logger = setup_logger("main")


async def main():
    conn = await init_db()
    if isinstance(conn, Exception):
        sys.exit(1)
    await dp.start_polling(bot)
    await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    logger.info("Start shut down")
    asyncio.run(shutdown())
