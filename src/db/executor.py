from logging import Logger
from typing import Awaitable, Optional, TYPE_CHECKING
from xml.dom.minidom import Identified

from tortoise.transactions import in_transaction

from db.models import UserModel, ItemsModel, EntityModel
from config import loggers


if TYPE_CHECKING:
    from game.classes.entity import User as app_user
    from game.classes.items import Item
    from game.classes.entity import Entity


class UserDB:
    def __init__(self, tracking_database: "UserModel", logger: Logger):
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
        user = (
            await self.tracking_database
            .filter(id=user_id)
            .first()
        )
        if not user:
            return None
        return user
    
    async def remove(self, user_id) -> bool:
        async with in_transaction():
            user: UserModel | None = (
                await self.tracking_database
                .filter(id=user_id)
                .select_for_update()
                .first()
            )
            if not user:
                self.logger.error(f"Can`t delete user with {user_id} id from DB, user not found!")
                return False
            await user.delete()
            self.logger.info(f"Deleted user with id {user_id} from user db")
            return True
    
    async def update(self, user_object: "app_user"):
        async with in_transaction():
            data = (
                await self.tracking_database
                .filter(id=user_object.id)
                .select_for_update()
                .first()
            )
            if data:
                data.user_entity = user_object.to_dict()
                await data.save()
            else:
                await self.add(user_object.id, user_object)
    
    async def araise_database(self, token=None):
        await self.tracking_database.all().delete()


class ItemsDB:
    def __init__(self, tracking_database: ItemsModel, logger: Logger):
        self.tracking_database = tracking_database
        self.logger = logger

    async def add(self, item_object: "Item") -> bool:
        item_identificator = item_object.identificator
        if not item_identificator:
            return False
        data = await self.get(identificator=item_identificator)
        if data:
            return False
        item = await self.tracking_database.create(identificator=item_identificator, data=item_object.to_dict())
        await item.save()
        return True

    async def get(self, identificator: str) -> Optional[ItemsModel]:
        item = await self.tracking_database.filter(identificator=identificator).first()
        if not item:
            return None
        return item
    
    async def remove(self, identificator: str) -> bool:
        async with in_transaction():
            item = (
                await self.tracking_database
                .filter(identificator=identificator)
                .select_for_update()
                .first()
            )
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
        async with in_transaction():
            item_model = (
                await self.tracking_database
                .filter(identificator=item_identificator)
                .select_for_update()
                .first()
            )
            if item_model:
                item_model.data = item_object.to_dict()
                await item_model.save()
                return True
            else:
                await self.add(item_object)
                return True

    async def araise_database(self, token=None):
        await self.tracking_database.all().delete()


class EntityDB:
    def __init__(self, tracking_database: "EntityModel", logger: Logger) -> None:
        self.tracking_database = tracking_database
        self.logger = logger

    async def add(self, entity_object: "Entity") -> bool:
        identificator = entity_object.identificator
        if not identificator:
            self.logger.error(f"Entity must have entity.identificator: {entity_object}")
            return False
        data = await self.get(identificator=identificator)
        if data:
            self.logger.error(f"Entity with Identificator=[{identificator}] has all ready exist in DB. You can only update, get, remove this item.")
            return False
        entity = await self.tracking_database.create(identificator=identificator, data=entity_object.to_dict())
        await entity.save()
        self.logger.info(f"Created new entity in Entity_DB with identificator={identificator}")
        return True

    async def get(self, identificator: str) -> Optional[EntityModel]:
        entity = await self.tracking_database.filter(identificator=identificator).first()
        if not entity:
            return None
        return entity

    async def remove(self, identificator: str) -> bool:
        async with in_transaction():
            entity = (
                await self.tracking_database
                .filter(identificator=identificator)
                .select_for_update()
                .first()
            )
            if not entity:
                self.logger.error(f"Can`t delete entity with identificator=[{identificator}] from DB, entity not found!")
                return False
            await entity.delete()
            self.logger.info(f"Deleted entity with identificator=[{identificator}] from Entity_DB")
            return True

    async def update(self, entity_object: "Entity") -> bool:
        entity_identificator = entity_object.identificator
        if not entity_identificator:
            self.logger.warning(f"Item object have not item Identificator. {entity_object.to_dict()}")
            return False
        async with in_transaction():
            entity_model = (
                await self.tracking_database
                .filter(identificator=entity_identificator)
                .select_for_update()
                .first()
            )
            if entity_model:
                entity_model.data = entity_object.to_dict()
                await entity_model.save()
                return True
            else:
                await self.add(entity_object)
                return True

    async def araise_database(self, token=None):
        await self.tracking_database.all().delete()
