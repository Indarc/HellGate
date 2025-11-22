import asyncio

from server.classes.db.executor import DB
from db.models.test_user import User
from server.config import setup_logger
from server.classes.game.user_class import User as game_user
from server.classes.game.player import Player

from server.config import init_db

init_db()
test_user_db = DB(User, setup_logger("test.user.db"))

class TestUserDB:
    def test_add_new_user(self):
        catch = test_user_db.get(123)
        if catch is not None:
            __class__.test_user_db.clear_database("1uhjb04182yu9ifjno10189i2490h")

        __class__.test_user_db.add(123, game_user(123, Player("test")))