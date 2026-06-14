import asyncio
import sys
from typing import Awaitable

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from tortoise import Tortoise

from paths import ROOT_DIR, RESOURCES_DIR

from loggers import Loggers


messages = {
    "hello_message": open(RESOURCES_DIR / "txt" / "hello_message.txt", encoding="utf-8").read()
}

class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr

    CONN: SecretStr
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: SecretStr
    POSTGRES_PORT: SecretStr
    POSTGRES_DB: SecretStr

    DB_CLEAR_PASSWORD: SecretStr

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8"
    )


config = Config()  # type: ignore[call-arg]
loggers = Loggers()

# DB_URL = f"{config.CONN.get_secret_value()}://{config.POSTGRES_USER.get_secret_value()}:{config.POSTGRES_PASSWORD.get_secret_value()}@{config.POSTGRES_HOST.get_secret_value()}:{config.POSTGRES_PORT.get_secret_value()}/{config.POSTGRES_DB.get_secret_value()}"

loggers.config.info("Start connecting bot")
try:
    storage = MemoryStorage()
    bot = Bot(config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher(storage=storage)
    loggers.config.info("Bot connection successed")
except Exception as ex:
    loggers.config.error(f"Bot connection refused. Error: {ex}")
    loggers.config.info("Stopping app")
    sys.exit(1)

# создание инструмента для работы с DB
# import DB and User model now that loggers is available
from db import executor, UserModel, ItemsModel

user_db = executor.UserDB(tracking_database=UserModel, logger=loggers.user_db_logger)
items_db = executor.ItemsDB(tracking_database=ItemsModel, logger=loggers.items_db_logger)

async def init_db():
    try:
        await Tortoise.init(config=TORTOISE_ORM)
        try:
            conn = Tortoise.get_connection(connection_name="default")
            await conn.execute_query("SELECT 1")
            loggers.config.info("✔️ Tortoise connection successed")
        except Exception as e:
            loggers.config.error(f"❌ Tortoise connection error: {e}")
            return e
        # Проверка, что модели загружены
        models = Tortoise.apps.get("models")
        if not models:
            raise Exception("No models found in Tortoise ORM")
        loggers.config.info(f"✔️ Models: {list(models.keys())}")
        
    except Exception as e:
        loggers.config.error(f"❌ Error: {e}")
        return e

async def shutdown():
    from game import game_manager
    try:
        await asyncio.sleep(0.5)
        await game_manager.user_manager.save_data()
        await asyncio.sleep(0.5)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # loggers.main.warning("Agree! Araising database is on.")
        # await user_db.araise_database()
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # await asyncio.sleep(0.5)
        await Tortoise.close_connections()
        loggers.config.info("Connections closed")
        await asyncio.sleep(0.5)
        await bot.session.close()
        loggers.config.info("Bot connection closed")
    except Exception as e:
        loggers.config.error(f"Error during shutdown: {e}")
    finally:
        await asyncio.sleep(0.5)

TORTOISE_ORM = {
    "connections": {"default": config.DB_URL.get_secret_value()},
    "apps": {
        "models": {
            "models": [
                "db.models.user",
                "db.models.items",
                "db.models.test_user",
                "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}