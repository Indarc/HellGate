from logging import Logger
from typing import Optional, TYPE_CHECKING

from db.models import UserModel, ItemsModel
from config import loggers

if TYPE_CHECKING:
    from game.classes.entity import User as app_user
    from game.classes.items import Item


class UserDB:
    def __init__(self, tracking_database, logger: Logger):
        self.tracking_database: "UserModel" = tracking_database
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


class ItemsDB:
    def __init__(self, tracking_database, logger: Logger):
        self.tracking_database: "ItemsModel" = tracking_database
        self.logger = logger

    async def add(self, item_object: "Item") -> bool:
        item_identificator = item_object.identificator
        if not item_identificator:
            loggers.items_db_logger.error(f"Item entity must have item.identificator: {item_object}")
            return False
        data = await self.get(identificator=item_identificator)
        if data:
            self.logger.error(f"Item with Identificator=[{item_identificator}] has all ready exist in DB. You can only update, get, remove this item.")
            return False
        item = await self.tracking_database.create(identificator=item_identificator, item_dict=item_object.to_dict())
        await item.save()
        self.logger.info(f"Created new item in ITEM_DB with identificator={item_identificator}")
        return True

    async def get(self, identificator: str) -> Optional[ItemsModel]:
        item = await self.tracking_database.filter(identificator=identificator).first()
        if not item:
            return None
        return item
    
    async def remove(self, identificator: str) -> bool:
        item: Optional["ItemsModel"] = await self.get(identificator=identificator)
        if not item:
            self.logger.error(f"Can`t delete item with identificator=[{identificator}] from DB, item not found!")
            return False
        await item.delete()
        self.logger.info(f"Deleted item with identificator=[{identificator}] from Item_DB")
        return True

    async def update(self, item_object: "Item") -> bool:
        item_identificator = item_object.identificator
        if not item_identificator:
            self.logger.warning(f"Item object have not item Identificator. {item_object.to_dict()}")
            return False
        data = await self.get(item_identificator)
        if data:
            data.item_dict = item_object.to_dict()
            await data.save()
            return True
        else:
            await self.add(item_object)
            return True

    async def araise_database(self, token=None):
        await self.tracking_database.all().delete()