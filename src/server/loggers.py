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
    config = setup_logger("config")
    main = setup_logger("main")
    game = setup_logger("game.logger")
    game_handlers = setup_logger("handlers.game.logger")
    game_classes = setup_logger("game.classes.logger")
    user_db_logger = setup_logger("user.db.logger")
    inventory_logger = setup_logger("game.inventory.logger")
    hero_creation_logger = setup_logger("hero.creation.logger")
    middlewares_logger = setup_logger("middlewares.logger")
    tests_logger = setup_logger("tests.logger")
    quest_logger = setup_logger("quest.logger")
    user_manager_logger = setup_logger("game.user_manager.logger")
