import logging
import sys
from pathlib import Path

from paths import ROOT_DIR

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
    file_handler = logging.FileHandler(filename=f"{ROOT_DIR}/logs.log", encoding='utf-8')
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
    def __init__(self):
        self.main = setup_logger("main")
        self.config = setup_logger("config")
        self.user_db_logger = setup_logger("db.user")
        self.items_db_logger = setup_logger("db.items")
        self.entity_db_logger = setup_logger("db.entity")
        self.game = setup_logger("game")
        self.game_handlers = setup_logger("game.handlers")
        self.game_classes = setup_logger("game.classes")
        self.inventory_logger = setup_logger("game.inventory")
        self.hero_creation_logger = setup_logger("game.hero_creation")
        self.middlewares_logger = setup_logger("bot_middlewares")
        self.tests_logger = setup_logger("tests")
        self.quest_logger = setup_logger("game.quest")
        self.game_manager_logger = setup_logger("game.game_manager")
        self.user_manager_logger = setup_logger("game.user_manager")
        self.item_manager_logger = setup_logger("game.item_manager")
        self.entity_manager_logger = setup_logger("game.entity_manager")
        self.interface_logger = setup_logger("game.interaface")
        self.bot_handlers = setup_logger("bot.handlers")
