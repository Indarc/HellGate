from typing import TYPE_CHECKING, Optional

from game.classes.items.affixes import Affixes

if TYPE_CHECKING:
    from game.classes.entity import Entity


class Item: # base class for all items
    """Default item class"""
    def __init__(self, data: Optional[dict]=None):
        self.type = data.get("type", "null") if data else "null"
        self.identificator: str = data.get("identificator", "null") if data else "null"
        self.name: str = data.get("name", "Undefined item") if data else "Undefined item"
        self.rarity: str = data.get("rare", "common") if data else "common"
        self.value: float = data.get("value", 0) if data else 0
        self.description: str = data.get("description", "No description") if data else "No description"
        self.emoji: str = data.get("emoji", "❔") if data else "❔"
        self.stacked: bool = data.get("stacked", False) if data else False
    
    def interface(self, count: int) -> list[str]:
        info = [
            f"{self.emoji if self.emoji else '❔'}{self.name}",
            f"⭐ Редкость: {self.rarity.capitalize()}",
            f"💬 Описание:\n{self.description}",
            f"👜 Колличество: {count}\n💰 Ценность: {self.value}⭐"
        ]
        return info

    def to_dict(self) -> dict:
        return {
            "identificator": self.identificator,
            "type": self.type,
            "name": self.name,
            "rare": self.rarity,
            "value": self.value,
            "description": self.description,
            "emoji": self.emoji,
            "stacked": self.stacked,
        }


class EquipItem(Item):
    def __init__(self, data: Optional[dict]=None):
        super().__init__(data)
        self.affixes = Affixes(data.get("affixes", {}), self.rarity if self.rarity else "common") if data else Affixes()
        self.equip_requirements = EquipRequirements(data.get("equip_requirements", {})) if data else EquipRequirements()
        self.slot: str = data.get("slot", "") if data else ""
        self.durability: Durability = Durability(data=data.get("durability", {})) if data else Durability()

    def is_broken(self) -> bool:
        return self.durability.status()
    
    def to_dict(self) -> dict:
        item_dict = super().to_dict()
        EquipItem_dict = {
            "affixes": self.affixes.to_dict(),
            "equip_requirements": self.equip_requirements.to_dict(),
            "slot": self.slot,
            "durability": self.durability.to_dict()
        }
        item_dict.update(EquipItem_dict)
        return item_dict

class EquipItemStats:
    def __init__(self, stats: Optional[dict]=None) -> None:
        self.upgrade: int = stats.get("upgrade", 0) if stats else 0

    def to_dict(self):
        return {
            "upgrade": self.upgrade
        }

class EquipRequirements:
    def __init__(self, data: Optional[dict]=None) -> None:
        self.level = data.get("level", 1) if data else 1
        self.strength = data.get("strength", 0) if data else 0
        self.agility = data.get("agility", 0) if data else 0
        self.intelligence = data.get("intelligence", 0) if data else 0
    
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
            self, durability: int=0, max_durability: int=0,
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

    def to_dict(self) -> dict:
        return {
            "durability": self.durability,
            "max_durability": self.max_durability
        }