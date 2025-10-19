import asyncio

from server.config import bot, dp, setup_logger, lifespan
from server.bot.handlers import setup_routers


dp.include_router(setup_routers())

logger = setup_logger("main")


async def main():
    await lifespan()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    logger.info("Shut down")
