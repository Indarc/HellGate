from logging import Logger

from db.models.user import User, UserShema
from server.classes.game.user_class import User as app_user


class DB:
    def __init__(self, tracking_database: User, logger: Logger):
        self.tracking_database = tracking_database
        self.logger = logger
    
    async def add(self, id, user_entity: app_user):
        user = await self.tracking_database.create(id=id, user_entity=user_entity.to_dict())
        await user.save()
        self.logger.info(f"Created new user with id {user_entity.id}")
    
    async def get(self, user_id: int) -> app_user:
        user = await self.tracking_database.filter(id=user_id).first()

        user = User(data=user, id=user_id)

        return user
    
    async def remove(self, user_id):
        user = await self.get(user_id)
        await user.delete()
        self.logger.info(f"Deleted user with id {user_id} from user db")
    
    async def edit(self, user_id):
        ...
    
    async def clear_database(self) -> bool:
        all_users = await self.tracking_database.all()
        for user in all_users:
            await user.delete()
        return True
    