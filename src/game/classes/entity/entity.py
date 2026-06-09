from typing import Optional, TYPE_CHECKING

from game.classes.items.damages import Damage
from config import loggers

from .equipment import Equipment
from .characteristicts import Level, Attributes, Characteristics
from game.classes.inventory.error_class import DontEnoughSlotsError
from game.classes.inventory.inventory import Inventory
from game.classes.items.item import EquipItem
from game.classes.items import *

if TYPE_CHECKING:
    from game.manager import AttackResult


class Entity:
    def __init__(self, name: Optional[str]=None, level: int=1, data: Optional[dict] = None):
        if not name and not data:
            loggers.game_classes.error("[ENTITY_INIT] Entity object requered paramateres to initializating")
            return
        self.entity_type = data.get("entity_type", "entity") if data else "entity"
        self.name: str = data.get("name", "Unknow") if data else name if name else "Unknow"
        self.inventory = Inventory(data=data.get("inventory")) if data else Inventory()
        self.attributes: Attributes = Attributes(data=data.get("attributes")) if data else Attributes()
        self.equipment: Equipment = Equipment(data=data.get("equipment")) if data else Equipment()
        self.characteristics: Characteristics = Characteristics(self.attributes, self.equipment, data.get("resistances", {}) if data else {})
        self.level: Level = Level(data=data.get("level", {}), tracking_attributes=self.attributes) if data else Level(tracking_attributes=self.attributes)

    def equip_item(self, item: Optional[EquipItem]=None, slot_id: Optional[int]=None) -> bool:
        # 1. проверка характеристик
        # 2. проверка места в инвентаре при наличии надетого снаряжения, далее его добавление в инвентарь
        item_to_equip = item
        if slot_id is not None:
            extracted_item_tuple = self.inventory.extract_item(slot_id)
            if not extracted_item_tuple:
                # TODO send message to player
                return False
            item_to_equip = extracted_item_tuple[0]
            if not isinstance(item_to_equip, EquipItem):
                # TODO send message to player, about that item can`t be equiped`
                return False
        if not item_to_equip:
            return False
        # 1
        requirements_status = item_to_equip.equip_requirements.check_entity_attributes(self)
        if not requirements_status:
            # TODO send message to player about characteristics requirements
            loggers.game_classes.debug(f"Player doesn't meet the requirements for equipping item id {item_to_equip.id} and requirements {item_to_equip.equip_requirements}")
            return False
        # 2
        previos_equiped_item = self.equipment.get_equip(item_to_equip.slot)
        if previos_equiped_item:
            try:
                self.inventory.add_item(previos_equiped_item)
            except DontEnoughSlotsError as e:
                # TODO send message to player about inventory full
                return False
        #
        self.equipment.equip_item(item_to_equip)
        return True
    
    def unequip_item(self, slot: str) -> bool:
        if self.inventory.get_free_space() == 0:
            return False
        item = self.equipment.unequip_item(slot)
        if not item:
            return False
        self.inventory.add_item(item)
        return True


    def get_level(self) -> int:
        return self.level.get_level()

    def get_health(self) -> float:
        return self.characteristics.get_health()

    def get_max_health(self) -> float:
        return self.characteristics.get_max_health()
    
    def get_damage(self) -> Damage:
        """Returns total damage with all buffs and attribute effects"""
        return self.characteristics.get_weapon_damage()
    
    def get_armor_rating(self) -> int:
        return self.characteristics.get_armor_rating()

    def get_evasion_rating(self) -> int:
        return self.characteristics.get_evasion_rating()
    
    def get_evasion_chance(self, enemy: "Entity") -> float:
        return self.characteristics.get_evasion_chance(enemy)
    
    def get_accuracy_rating(self) -> int:
        return self.characteristics.get_evasion_rating()
    
    def get_hit_chance(self, enemy: "Entity") -> float:
        enemy_evasion = enemy.get_evasion_rating()
        self_accuracy = self.get_accuracy_rating()
        if enemy_evasion == 0:
            return 100.0
        hit_chance = self_accuracy / (enemy_evasion / 100)
        return hit_chance

    def try_evade(self, attacker: "Entity") -> bool:
        from random import  randint
        hit_chance = attacker.get_hit_chance(self)
        rnd = randint(0, 101)
        if hit_chance >= rnd:
            return True
        return False

    def add_experience(self, exp: int) -> None:
        self.level.add_exp(exp)

    def check_alive(self) -> bool:
        return self.characteristics.check_alive()

    def attack(self, target: "Entity") -> "AttackResult":
        from game.manager import AttackResult
        weapon = self.equipment.get_equip("mainhand")
        if not weapon or not isinstance(weapon, Weapon):
            return AttackResult()
        evade_status = target.try_evade(self)
        if evade_status:
            return AttackResult(evaded=True)
        return target.take_damage(weapon)

    def take_damage(self, weapon: Weapon) -> "AttackResult":
        # TODO evasion chance
        # TODO поломка снаряжения
        attack_result = self.characteristics.take_damage(weapon)
        return attack_result

    def battle_banner(self, enemy: "Entity") -> str:
        text = f"""
❤️HP: [{self.characteristics.health}/{self.get_max_health()}]
Имя: {self.name}
Уровень: {self.level.get_level()}

⚔️Урон: {self.get_damage().to_dict()}
🛡️Броня: {self.get_armor_rating()}
👟Уклонение: {self.get_evasion_chance(enemy)}%
🎯Точность: {self.get_hit_chance(enemy)}%
"""
        return text
    
    def to_dict(self) -> dict:
        return {
            "_": "Entity",
            "name": self.name,
            "inventory": self.inventory.to_dict(),
            "attributes": self.attributes.to_dict(),
            "equipment": self.equipment.to_dict(),
            "characteristics": self.characteristics.to_dict(),
            "level": self.level.to_dict(),
        }