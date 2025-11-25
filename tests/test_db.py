import asyncio

from db.executor import DB
from db.models.test_user import TestUser
from server.loggers import Loggers
from game.classes.entity.user_class import User
from game.classes.entity.player import Player

from server.config import init_db

init_db()
test_user_db = DB(User, Loggers.tests_logger)

class TestUserDB:
    def test_add_new_user(self):
        catch = test_user_db.get(123)
        if catch is not None:
            __class__.test_user_db.clear_database("1uhjb04182yu9ifjno10189i2490h")

        __class__.test_user_db.add(123, User(123, Player("test")))