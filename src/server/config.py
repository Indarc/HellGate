import logging
from pathlib import Path
import sys

from aiogram import Bot, Dispatcher
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from tortoise import Tortoise

ROOT_DIR = Path(__file__).parent.parent

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

logger = setup_logger("config")

class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / "server" / ".env",
        env_file_encoding="utf-8"
    )

config = Config()

logger.info("Start connecting bot")
try:
    bot = Bot(config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    logger.info("Bot connection successed")
except Exception as ex:
    logger.error(f"Bot connection refused. Error: {ex}")
    logger.info("Stopping app")
    sys.exit(1)

async def lifespan():
    await Tortoise.init(TORTOISE_ORM)
    logger.info("Tortoise connection successed")
    yield
    logger.info("Start clossing sessions...")
    await Tortoise.close_connections()
    logger.info("Tortoise session closed")
    await bot.session.close()
    logger.info("Bot session closed")



TORTOISE_ORM = {
    "connections": {"default": config.DB_URL.get_secret_value()},
    "apps": {
        "models": {
            "models": [
                "db.models.user",
                "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}