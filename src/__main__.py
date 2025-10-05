import asyncio

from config import bot, dp, setup_logger
from server.bot.handlers import setup_routers


dp.include_router(setup_routers())

logger = setup_logger("main")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    logger.info("Shut down")
