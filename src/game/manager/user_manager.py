from logging import Logger

from db.executor import UserDB
from config import ROOT_DIR, loggers

from game.classes.entity import User


PLAYERS_TEMP_FOLDER = ROOT_DIR / "game" / "temp" / "players"
FILE_EXTANSION = ".json"

class UserManager:
    def __init__(self, user_db_executor: UserDB, logger: Logger):
        self.users: dict[int, User] = {}
        self.user_db_executor = user_db_executor
        self.logger = logger

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
            self.logger.error("Can`t update user in DB, user object not found in self.users")
            return
        await self.user_db_executor.update(user)
    
    async def load_user(self, user_id: int) -> User | None:
        user = self.users.get(user_id)
        if not user:
            user_model = await self.user_db_executor.get(user_id)
            if not user_model:
                self.logger.error(f"Can`t load user with id {user_id} from DB, user not found")
                # TODO: перенаправление пользователя на создание персонажа, если он не найден в БД
                # создание текст и клавиатуры для перенаправления на создание персонажа
                return None
            user_object = User(user_model.id, user_model.user_entity)
            self.users.update({user_model.id: user_object})
        return self.users[user_id]
        
    async def save_data(self):
        for user_id in self.users.keys():
            await self.update_user_in_db(user_id)
        self.logger.info("✔️Successfull export users to DB")