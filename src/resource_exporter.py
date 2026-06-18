import asyncio
import json
from pathlib import Path

from config import RESOURCES_DIR
from game import game_manager
from game.classes.items import Weapon, Material, Item
from game.classes.entity import Entity, Enemy
from config import RESOURCES_DIR, init_db


class App:
    def __init__(self) -> None:
        self.items_path = RESOURCES_DIR / "items"
        self.entity_path  = RESOURCES_DIR / "entity"
        self.item_manager = game_manager.item_manager
        self.entity_manager = game_manager.entity_manager

    async def save(self):
        await init_db()
        await self.save_items()
        await self.save_entity()

    async def save_items(self):
        async def add(item: Item):
            try:
                await self.item_manager.add(item)
            except Exception as e:
                self.item_manager.logger.error(f"Error with save item to database: {e}")

        json_files = list(self.items_path.glob("*.json"))
        for file in json_files:
            with open(file, encoding="utf-8") as file:
                items_list: list[dict] = json.load(file)
                for item_data in items_list:
                    item = self.item_manager.dti(item_data)
                    if not item:
                        continue
                    await add(item)

    async def save_entity(self):
        async def add(entity: Entity):
            try:
                await self.entity_manager.add(entity)
            except Exception as e:
                self.entity_manager.logger.error(f"Error with save entity to database: {e}")
        json_files = list(self.entity_path.glob("*.json"))
        for file in json_files:
            with open(file, encoding="utf-8") as file:
                entity_list: list[dict] = json.load(file)
                for entity_data in entity_list:
                    entity = self.entity_manager.dte(entity_data)
                    if not entity:
                        continue
                    await add(entity)
    
if __name__ == "__main__":
    app = App()
    asyncio.run(app.save())
