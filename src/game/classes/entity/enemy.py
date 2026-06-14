from typing import Optional

from .entity import Entity


class Enemy(Entity):
    def __init__(self, name: Optional[str] = None, level: int = 1, data: Optional[dict] = None):
        super().__init__(name, level, data)
        # TODO: add loot, experience for kill, maybe some unique skills and stuff like that
        self.damage = data.get("damage", 0) if data else 0
        self.armor = data.get("armor", 0) if data else 0
        self.description: str = data.get("description", "") if data else ""
        self.drop = data.get("drop", []) if data else []