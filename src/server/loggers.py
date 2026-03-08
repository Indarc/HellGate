import logging
import sys
from pathlib import Path

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

class Loggers:
    def __init__(self):
        self.main = setup_logger("main.logger")
        self.config = setup_logger("config.logger")
        self.game = setup_logger("game.logger")
        self.game_handlers = setup_logger("handlers.game.logger")
        self.game_classes = setup_logger("game.classes.logger")
        self.user_db_logger = setup_logger("user.db.logger")
        self.inventory_logger = setup_logger("game.inventory.logger")
        self.hero_creation_logger = setup_logger("hero.creation.logger")
        self.middlewares_logger = setup_logger("middlewares.logger")
        self.tests_logger = setup_logger("tests.logger")
        self.quest_logger = setup_logger("quest.logger")
        self.game_manager_logger = setup_logger("game.game_manager.logger")
        self.user_manager_logger = setup_logger("game.user_manager.logger")
        self.item_manager_logger = setup_logger("game.item_manager.logger")
