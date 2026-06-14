from typing import Optional

from game.classes.items import *
from game.classes.items.item import EquipItem
from config import loggers


class Equipment:
    def __init__(self, data: Optional[dict] = None):
        self.mainhand: Optional[Weapon] = Weapon(data = data.get("mainhand", {})) if data and data.get("main_weapon") else None
        self.offhand: Optional[Weapon] = Weapon(data = data.get("offhand", {})) if data and data.get("offhand_weapon") else None
        self.twohand: Optional[Weapon] = Weapon(data = data.get("twohand", {})) if data and data.get("offhand_weapon") else None
        self.head = None
        self.body: Optional[Armor] = None
        self.legs = None
        self.boots = None
        self.gloves = None
        self.cloak = None
        self.belt = None
        self.ring1 = None
        self.ring2 = None
        self.amulet = None
        self.bag: Optional[Bag] = Bag(data=data.get("bag", {})) if data and data.get("bag") else None

    def equip_item(self, item: EquipItem) -> Optional[EquipItem]:
        if item.type not in ["weapon", "armor", "jewelry", "bag"]:
            loggers.game_classes.error(f"Undefined item type {type(item)} to equiping")
            return
        if not isinstance(item, (Weapon, Armor, Jewelry, Bag)):
            loggers.game_classes.error(f"Undefined item class {type(item)} to equiping")
            return
        previos_equiped_item = self.unequip_item(slot=item.slot)
        if item.type == "weapon":
            item_slot = item.slot
            if item_slot == "twohand":
                mainhand_weapon = self.get_equip(slot="mainhand")
                if mainhand_weapon:
                    previos_equiped_item = self.unequip_item(slot="mainhand")
            elif item_slot == "mainhand" or item_slot == "offhand":
                twohand_weapon = self.get_equip(slot="twohand")
                if twohand_weapon:
                    previos_equiped_item = self.unequip_item(slot="twohand")
        setattr(self, item.slot, item)
        return previos_equiped_item

    def unequip_item(self, slot: str) -> Optional[EquipItem]:
        item: EquipItem | None = self.get_equip(slot)
        if not item:
            return None # raise empty slot exception
        
        setattr(self, slot, None)
        return item
    
    def get_equip(self, slot: str) -> Optional[EquipItem]:
        return getattr(self, slot, None)

    def get_health_buff(self) -> dict[str, int]:
        hp_buffes = {}
        for slot, item in self.__dict__.items():
            if slot in ["mainhand", "bag"] or item is None:
                continue
            item_buffes: dict[str, dict] = item.affixes.get_buffes()
            max_health_buffes = item_buffes.get("max_health", {})
            hp_buffes.update(max_health_buffes)
        return hp_buffes

    def get_evasion(self) -> int:
        total_evasion = 0
        for slot, item in self.__dict__.items():
            if slot not in ["head", "body", "legs", 
                            "boots", "gloves", "cloak"] or item is None:
                continue
            total_evasion += item.stats.get_evasion_rating()
        return total_evasion
    
    def get_armor(self) -> int:
        total_armor = 0
        for slot, item in self.__dict__.items():
            if slot not in ["head", "body", "legs", 
                            "boots", "gloves", "cloak"] or item is None:
                continue
            total_armor += item.stats.get_armor_rating()
        return total_armor
    
    def get_equipment(self) -> dict:
        return self.__dict__

    def to_dict(self) -> dict:
        """Return dictionary with equiped items

        Returns :
            dict: {item_slot (str), item[Item] | None}
        """
        return {
            "mainhand": self.mainhand.to_dict() if self.mainhand else None,
            "offhand": self.offhand.to_dict() if self.offhand else None,
            "twohand": self.twohand.to_dict() if self.twohand else None,
            "head": self.head.to_dict() if self.head else None,
            "body": self.body.to_dict() if self.body else None,
            "legs": self.legs.to_dict() if self.legs else None,
            "boots": self.boots.to_dict() if self.boots else None,
            "gloves": self.gloves.to_dict() if self.gloves else None,
            "cloak": self.cloak.to_dict() if self.cloak else None,
            "belt": self.belt.to_dict() if self.belt else None,
            "ring1": self.ring1.to_dict() if self.ring1 else None,
            "ring2": self.ring2.to_dict() if self.ring2 else None,
            "amulet": self.amulet.to_dict() if self.amulet else None,
            "bag": self.bag.to_dict() if self.bag else None
        }