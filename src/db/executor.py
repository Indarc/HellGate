from ast import Delete
from logging import Logger
from typing import Optional, Type, TYPE_CHECKING

from db.models.user import UserModel, UserShema
from config import loggers

if TYPE_CHECKING:
    from game.classes.entity.user_class import User as app_user


class DB:
    def __init__(self, tracking_database: UserModel, logger: Logger):
        self.tracking_database = tracking_database
        self.logger = logger
    
    async def add(self, id, user_entity: "app_user"):
        data = await self.get(id)
        if data:
            loggers.user_db_logger.error(f"User with {id} ID already exists in DB, can`t create new user with this id")
            return
        user = await self.tracking_database.create(id=id, user_entity=user_entity.to_dict())
        await user.save()
        self.logger.info(f"Created new user with id {user_entity.id}")
    
    async def get(self, user_id: int) -> Optional[UserModel]:
        user = await self.tracking_database.filter(id=user_id).first()
        if not user:
            return None
        return user
    
    async def remove(self, user_id) -> bool:
        user: UserModel | None = await self.get(user_id)
        if not user:
            self.logger.error(f"Can`t delete user with {user_id} id from DB, user not found!")
            return False
        await user.delete()
        self.logger.info(f"Deleted user with id {user_id} from user db")
        return True
    
    async def update(self, user_object: "app_user"):
        data = await self.tracking_database.filter(id=user_object.id).first()
        if data:
            data.user_entity = user_object.to_dict()
            await data.save()
        else:
            await self.add(user_object.id, user_object)
    
    async def araise_database(self, token=None):
        await self.tracking_database.all().delete()