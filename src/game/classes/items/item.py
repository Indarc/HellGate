from typing import TYPE_CHECKING, Optional

from game.classes.items.affixes import Affixes

if TYPE_CHECKING:
    from game.classes.entity import Entity


class Item: # base class for all items
    """Default item class"""
    def __init__(self, data: dict):
        self.item_type = data.get("item_type", "another")
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "Undefined item")
        self.rarity: str = data.get("rare", "common")
        self.cost: float = data.get("cost", 0)
        self.description: str = data.get("description", "No description")
        self.emoji: str = data.get("emoji", "❔")
        self.stacked: bool = data.get("stacked", False)
    
    def interface(self, count: int) -> list[str]:
        info = [
            f"{self.emoji if self.emoji else '❔'}{self.name}",
            f"⭐ Редкость: {self.rarity.capitalize()}\n💰 Цена: {self.cost} монет",
            f"💬 Описание:\n{self.description}",
            f"👜 Колличество: {count}"
        ]
        return info

    def to_dict(self) -> dict:
        return {
            "item_type": self.item_type,
            "id": self.id,
            "name": self.name,
            "rare": self.rarity,
            "cost": self.cost,
            "description": self.description,
            "emoji": self.emoji,
            "stacked": self.stacked,
        }


class EquipItem(Item):
    def __init__(self, data: dict):
        super().__init__(data)
        self.affixes = Affixes(data.get("affixes", {}), self.rarity if self.rarity else "common")
        self.equip_requirements = EquipRequirements(data.get("equip_requirements", {}))
        self.slot: str = data.get("slot", "")
        self.durability: Durability = Durability(data=data.get("durability", {}))
    
    def to_dict(self) -> dict:
        item_dict = super().to_dict()
        EquipItem_dict = {
            "affixes": self.affixes.to_dict(),
            "equip_requirements": self.equip_requirements.to_dict(),
            "slot": self.slot
        }
        item_dict.update(EquipItem_dict)
        return item_dict

class EquipItemStats:
    def __init__(self, stats: dict) -> None:
        self.upgrade: int = stats.get("upgrade", 0)

class EquipRequirements:
    def __init__(self, data: dict) -> None:
        self.level = data.get("level", 1)
        self.strength = data.get("strength", 0)
        self.agility = data.get("agility", 0)
        self.intelligence = data.get("intelligence", 0)
    
    def check_entity_attributes(self, entity: "Entity") -> bool:
        if entity.get_level() < self.level:
            return False
        if entity.attributes.get_agility() < self.agility:
            return False
        if entity.attributes.get_intelligence() < self.intelligence:
            return False
        if entity.attributes.get_strength() < self.strength:
            return False
        return True

    def to_dict(self) -> dict:
        return {
            "_": "EquipRequirements",
            "level": self.level,
            "strength": self.strength,
            "agility": self.agility,
            "intelligence": self.intelligence
        }
    

class Durability:
    def __init__(
            self, durability: int=1000, max_durability: int=1000,
            data: Optional[dict]=None
        ) -> None:
        self.durability = data.get("durability", 0) if data else durability
        self.max_durability = data.get("max_durability", 0) if data else max_durability
    
    def crack(self, value: int=3):
        self.durability -= value
    
    def repair(self):
        self.durability = self.max_durability

    def status(self) -> bool:
        if self.durability <= 1:
            return False
        else:
            return True