from typing import Optional

from db.executor import DB
from game.classes.entity.user_class import User
from server.config import ROOT_DIR, loggers


PLAYERS_TEMP_FOLDER = ROOT_DIR / "game" / "temp" / "players"
FILE_EXTANSION = ".json"

class UserManager:
    def __init__(self, user_db_executor: DB):
        self.users: dict[int, User] = {}
        self.user_db_executor = user_db_executor

    async def save_user(self, user_object: User) -> bool:
        if self.users.get(user_object.id):
            self.users.update({user_object.id: user_object})
            await self.update_user_in_db(user_object.id)
            return True
        else:
            self.users.setdefault(user_object.id, user_object)
            await self.update_user_in_db(user_object.id)
            return True
    
    async def update_user_in_db(self, user_id):
        user = self.users.get(user_id)
        if not user:
            loggers.user_manager_logger.error("Can`t update user in DB, user object not found in self.users")
            return
        await self.user_db_executor.update(user)
    
    async def load_user(self, user_id: int) -> User | None:
        data = self.users.get(user_id)
        if not data:
            data = await self.user_db_executor.get(user_id)
            if not data:
                loggers.user_manager_logger.error(f"Can`t load user with id {user_id} from DB, user not found")
                # TODO: перенаправление пользователя на создание персонажа, если он не найден в БД
                # создание текст и клавиатуры для перенаправления на создание персонажа
                return None
            user_object = User(data.user_entity.id, data.user_entity)
            self.users.setdefault(data.id, user_object)
            return self.users[user_id]
        if data:
            return self.users[data.id]
        else: return None
        
    async def save_data(self):
        for user_id in self.users.keys():
            await self.update_user_in_db(user_id)
        loggers.user_manager_logger.info("✔️Successfull export users to DB")