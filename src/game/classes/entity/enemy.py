from typing import Optional

from .entity import Entity


class Enemy(Entity):
    def __init__(self, name: Optional[str] = None, level: int = 1, data: Optional[dict] = None):
        super().__init__(name, level, data)
        # TODO: add loot, experience for kill, maybe some unique skills and stuff like that
        self.type = "enemy"
        self.level = data.get("level", 1) if data else level
        self.identificator = data.get("identificator", "enemy") if data else "enemy"
        self.description: str = data.get("description", "") if data else ""
        self.loot = data.get("loot", []) if data else []
        self.experience = data.get("experience", 0) if data else 0

    def get_level(self) -> int:
        return self.level

    def to_dict(self) -> dict:
        entity_dict = super().to_dict()
        entity_dict.update(
            {
                "_": "Enemy",
                "identificator": self.identificator,
                "description": self.description,
                "loot": self.loot,
                "experience": self.experience,
                "type": self.type
            }
        )
        return entity_dict