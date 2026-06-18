from logging import Logger
from typing import Optional

from config import loggers
from db.executor import EntityDB
from game.classes.entity import Entity, Enemy


class EntityManager:
    def __init__(self, entity_db_executor: EntityDB, logger: Logger) -> None:
        self.entity_classes = {
            "enemy": Enemy
        }
        self.entity = {}
        self.entity_db_executor = entity_db_executor
        self.logger = logger

    async def add(self, entity_object: Enemy):
        if not entity_object.identificator:
            self.logger.warning("To add new entity to DB, entity object must have uniq Identificator.")
            return
        if await self.get(entity_object.identificator):
            self.logger.warning(f"Entity with Identificator [{entity_object.identificator}] is already exist in DB.")
            return
        await self.entity_db_executor.add(entity_object=entity_object)
        self.logger.info(f"Created new Entity in Entity_DB with identificator={entity_object.identificator}")

    async def get(self, identificator: str):
        entity_local: Optional[Entity] = self.entity.get(identificator)
        if entity_local:
            return entity_local
        entity_model = await self.entity_db_executor.get(identificator)
        if not entity_model:
            self.logger.warning(f"Can`t get entity with identificator=[{identificator}]. Entity does not exist.")
            return
        entity_dict: dict = entity_model.data
        if not entity_dict:
            self.logger.warning(f"Entity [{entity_model.identificator}] from DB have not data field.")
            return
        entity_type = entity_dict.get("type")
        if not entity_type:
            self.logger.error(f"Entity dict have not type field: {entity_dict}")
            return
        entity_class = self.entity_classes.get(entity_type)
        if not entity_class:
            self.logger.error(f"Can`t find Entity class for [{entity_type}]")
            return
        entity: Entity = entity_class(data=entity_dict)
        if self.entity.__len__() < 100:
            self.entity.update({entity.identificator: entity})
        else:
            lambda: (k := next(iter(self.entity)), self.entity.pop(k))
            self.entity.update({entity.identificator: entity})
        return entity

    async def update(self, entity_object: Enemy) -> bool:
        entity_local: Enemy = self.entity.pop(entity_object.identificator, None)
        if entity_local:
            self.logger.info(f"Remove entity [{entity_local.identificator}] from local memory")
        if not await self.entity_db_executor.update(entity_object):
            self.logger.error("Fail to update entity in DB.")
            return False
        return True


    def dict_to_entity(self, entity_dict: dict) -> Optional[Entity]:
        """Convert item dict to item object"""
        entity_identificator = entity_dict.get("identificator")
        entity_type = entity_dict.get("type")
        if not entity_identificator or not entity_type:
            loggers.game.warning(f"Entity id or type not found in dict: {entity_dict}")
            return None
        entity_class = self.entity_classes.get(entity_type)
        if not entity_class:
            loggers.game.warning(f"Undefined entity type: {entity_type} in dict: {entity_dict}")
            return None
        entity = entity_class(data=entity_dict)
        return entity

    def dte(self, entity_dict: dict) -> Optional[Entity]:
        return self.dict_to_entity(entity_dict=entity_dict)

    