import asyncio
import sys

from server.config import bot, dp, init_db, shutdown
from server.loggers import Loggers
from server.bot.handlers import setup_routers

dp.include_router(setup_routers())

async def main():
    conn = await init_db()
    if isinstance(conn, Exception):
        sys.exit(1)
    
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        Loggers.config.info("Bot stopped by user")
    except Exception as e:
        Loggers.config.error(f"Unexpected error: {e}")
    finally:
        Loggers.config.info("Starting shutdown process...")
        await shutdown()

if __name__ == "__main__":
    asyncio.run(main())