import asyncio
import sys

from server.config import bot, dp, init_db, shutdown, loggers
from server.bot.handlers import setup_routers

dp.include_router(setup_routers())

async def main():
    conn = await init_db()
    if isinstance(conn, Exception):
        sys.exit(1)
    
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        loggers.config.info("Bot stopped by user")
    except Exception as e:
        loggers.config.error(f"Unexpected error: {e}")
    finally:
        loggers.config.info("Starting shutdown process...")
        await shutdown()

if __name__ == "__main__":
    asyncio.run(main())