import asyncio
import sys

from aiogram import Bot, Dispatcher
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from tortoise import Tortoise

from paths import ROOT_DIR, RESOURCES_DIR

from db.executor import DB
from db.models.user import User

from server.loggers import Loggers

from game.user_manager import UserManager


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
        env_file=ROOT_DIR / "server" / ".env",
        env_file_encoding="utf-8"
    )


config = Config()

DB_URL = f"{config.CONN.get_secret_value()}://{config.POSTGRES_USER.get_secret_value()}:{config.POSTGRES_PASSWORD.get_secret_value()}@{config.POSTGRES_HOST.get_secret_value()}:{config.POSTGRES_PORT.get_secret_value()}/{config.POSTGRES_DB.get_secret_value()}"

Loggers.config.info("Start connecting bot")
try:
    bot = Bot(config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    Loggers.config.info("Bot connection successed")
except Exception as ex:
    Loggers.config.error(f"Bot connection refused. Error: {ex}")
    Loggers.config.info("Stopping app")
    sys.exit(1)

# создание инструмента для работы с DB
user_db = DB(tracking_database=User, logger=Loggers.user_db_logger)
user_manager = UserManager(user_db_executor=user_db)

async def init_db():
    try:
        await Tortoise.init(config=TORTOISE_ORM)
        Loggers.config.info("✔️ Tortoise connection successed")

        # Проверка, что модели загружены
        Loggers.config.info(f"✔️ Models: {list(Tortoise.apps.get("models").keys())}")
        
    except Exception as e:
        Loggers.config.error(f"❌ Error: {e}")
        return e

async def shutdown():
    try:
        await asyncio.sleep(0.5)
        await user_manager.save_data()
        user_manager.clear_temp_folder()
        await asyncio.sleep(0.5)
        await Tortoise.close_connections()
        Loggers.config.info("Connections closed")
        await asyncio.sleep(0.5)
        await bot.session.close()
        Loggers.config.info("Bot connection closed")
    except Exception as e:
        Loggers.config.error(f"Error during shutdown: {e}")
    finally:
        await asyncio.sleep(0.5)

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": [
                "db.models.user",
                "db.models.test_user",
                "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}