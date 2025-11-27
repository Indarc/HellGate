from logging import Logger

from db.models.user import User, UserShema
from game.classes.entity.user_class import User as app_user
from server.loggers import Loggers


class DB:
    def __init__(self, tracking_database: User, logger: Logger):
        self.tracking_database = tracking_database
        self.logger = logger
    
    async def add(self, id, user_entity: app_user):
        data = await self.get(id)
        if data:
            Loggers.user_db_logger.error(f"User with {id} ID already exists in DB, can`t create new user with this id")
            return
        user = await self.tracking_database.create(id=id, user_entity=user_entity.to_dict())
        await user.save()
        self.logger.info(f"Created new user with id {user_entity.id}")
    
    async def get(self, user_id: int) -> app_user:
        user = await self.tracking_database.filter(id=user_id).first()
        if user:
            user_object = app_user(id=user_id, data=user.user_entity)
            return user_object
        else:
            return user
    
    async def remove(self, user_id):
        user: User = await self.get(user_id)
        await user.delete()
        self.logger.info(f"Deleted user with id {user_id} from user db")
    
    async def update(self, user_object: app_user):
        data = await self.tracking_database.filter(id=user_object.id).first()
        if data:
            data.user_entity = user_object.to_dict()
            await data.save()
        else:
            await self.add(user_object.id, user_object)
    
    async def clear_database(self) -> bool:
        all_users = await self.tracking_database.all()
        for user in all_users:
            await user.delete()
        return True
    