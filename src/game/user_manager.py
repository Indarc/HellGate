import json
import aiofiles
import os.path

from db.executor import DB
from game.classes.entity.user_class import User
from server.config import ROOT_DIR
from server.loggers import Loggers


PLAYERS_TEMP_FOLDER = ROOT_DIR / "game" / "temp" / "players"
FILE_EXTANSION = ".json"

class UserManager:
    def __init__(self, user_db_executor: DB):
        self.users = {}
        self.user_db_executor = user_db_executor

    async def save_user(self, user_object: User) -> bool:
        if self.users.get(user_object.id):
            self.users.update(user_object.id, user_object)
            await self.update_user_in_db(user_object.id)
            await self.update_temp_folder(user_object.id)
            return True
        else:
            self.users.setdefault(user_object.id, user_object)
            await self.update_user_in_db(user_object.id)
            await self.update_temp_folder(user_object.id)
            return True
    
    async def update_user_in_db(self, user_id):
        user = self.users.get(user_id)
        if not user:
            Loggers.user_manager_logger.error("Can`t update user in DB, user object not found in self.users")
            return
        await self.user_db_executor.update(user)

    async def load_user(self, user_id: int, user_object: User=None) -> User | None:
        data: User = self.users.get(user_id)
        if not data:
            if os.path.exists(PLAYERS_TEMP_FOLDER / f"{user_id}{FILE_EXTANSION}"):
                async with aiofiles.open(PLAYERS_TEMP_FOLDER / f"{user_id}{FILE_EXTANSION}") as file:
                    data = await file.read()
                data = json.loads(data)
                data = User(id=user_id, data=data)
                self.users.setdefault(data.id, data)
                await self.update_temp_folder(data.id)
            else:
                data = await self.user_db_executor.get(user_id)
                if data:
                    self.users.setdefault(data.id, data)
                    await self.update_temp_folder(data.id)
        if data:
            user = self.users[data.id]
            return user
        else: return None
    
    async def update_temp_folder(self, user_id: int) -> bool:
        user: User = self.users.get(user_id)
        try:
            async with aiofiles.open(PLAYERS_TEMP_FOLDER / f"{user_id}{FILE_EXTANSION}", mode="w", encoding="utf-8") as file:
                await file.write(json.dumps(user.to_dict(), ensure_ascii=False))
            return True
        except Exception as e:
            Loggers.user_manager_logger.error(f"Error with update temp folder with new player: {e}")
            return False
    
    async def save_data(self):
        for user_id in self.users.keys():
            await self.update_user_in_db(user_id)
            await self.update_temp_folder(user_id)
        Loggers.user_manager_logger.info("✔️Successfull export users to DB")