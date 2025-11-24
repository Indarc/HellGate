import logging
from pathlib import Path
import sys

from aiogram import Bot, Dispatcher
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from tortoise import Tortoise

from server.classes.db.executor import DB
from db.models.user import User


ROOT_DIR = Path(__file__).parent.parent
RESOURCES_DIR = Path(__file__).parent.parent / "resources"

messages = {
    "hello_message": open(RESOURCES_DIR / "hello_message.txt").read()
}

def setup_logger(name: str) -> logging.Logger:
    # Создаем логгер
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.DEBUG)  # Устанавливаем минимальный уровень логирования

    # Создаем форматтер
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. Обработчик для записи в файл (сохраняет все сообщения от DEBUG и выше)
    file_handler = logging.FileHandler(f"{ROOT_DIR}/logs.log", encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 2. Обработчик для вывода в консоль (выводит только INFO и выше)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class Loggers:
    config = setup_logger("config")
    main = setup_logger("main")
    game_handlers = setup_logger("handlers.game.Loggers.config")
    game_classes = setup_logger("game.classes.Loggers.config")
    user_db_logger = setup_logger("user.db.Loggers.config")


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

async def init_db():
    try:
        await Tortoise.init(config=TORTOISE_ORM)
        Loggers.config.info("✅ Tortoise connection successed")

        # Проверка, что модели загружены
        Loggers.config.info(f"✅ Models: {list(Tortoise.apps.get("models").keys())}")
        
    except Exception as e:
        Loggers.config.error(f"❌ Error: {e}")
        return e

async def shutdown():
    await Tortoise.close_connections()
    Loggers.config.info("Connections closed")
    await bot.session.close()
    Loggers.config.info("Bot connection closed")

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