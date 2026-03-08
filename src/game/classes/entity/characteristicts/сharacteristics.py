from typing import TYPE_CHECKING

from game.classes.entity.resistances import Resistances
from game.classes.items.damages import Damage
from game.classes.items.weapon import Weapon

from ..entity import Equipment
from .attributes import Attributes

if TYPE_CHECKING:
    from ..entity import Entity


class Characteristics:
    """Класс для брони, урона, уклонения и тп"""
    def __init__(self, tracking_attributes: Attributes, tracking_equipment: Equipment, resistances: dict) -> None:
        self.tracking_attributes = tracking_attributes
        self.tracking_equipment = tracking_equipment
        self.resistances = Resistances(resistances)
        self.health = self.get_max_health()

    def get_max_health(self) -> int:
        default_hp = 20
        hp_from_strength = self.tracking_attributes.get_health_from_strength()
        hp_equipment_buffes = self.tracking_equipment.get_health_buff()
        additional_hp = 0
        for stat, value in hp_equipment_buffes.items():
            if stat == "strength":
                additional_hp += value * Attributes.streng_hp_multiplicator
            elif stat == "max_health":
                additional_hp += value
        total_hp = default_hp + hp_from_strength + additional_hp
        return total_hp
    
    def get_weapon_damage(self) -> Damage:
        # weapon damage + player attributes
        weapon = self.tracking_equipment.get_equip("mainhand")
        if not weapon: return Damage({})
        if isinstance(weapon, Weapon):
            return weapon.get_damage()
        else:
            return Damage({})

    def get_hit_chance(self, enemy: "Entity") -> float:
        accuracy_rating = self.get_accuracy_rating()
        enemy_evasion = enemy.get_evasion_rating()

        hit_chance = accuracy_rating - (enemy_evasion * 1.5)
        return float(hit_chance)
    
    def get_accuracy_rating(self) -> int:
        agility = self.tracking_attributes.get_agility() # 1 agility rating = 2 accuracy rating
        accuracy_rating = agility * 2
        return accuracy_rating

    def get_evasion_rating(self) -> int:
        # базовое уклонение зависит от процента уклонения на броне
        return self.tracking_equipment.get_total_evasion()
    
    def get_evasion_chance(self, enemy: "Entity") -> float:
        ...

    def get_armor(self) -> int:
        return self.tracking_equipment.get_armor()

    def take_damage(self, dmg: Damage) -> bool:
        self.health -= dmg.physical.get_value()
        self.health -= dmg.fire.get_value() - (dmg.fire.get_value() / 100 * self.resistances.fire.get_value())
        self.health -= dmg.cold.get_value() - (dmg.cold.get_value() / 100 * self.resistances.cold.get_value())
        self.health -= dmg.lightning.get_value() - (dmg.lightning.get_value() / 100 * self.resistances.lightning.get_value())
        return self.check_alive()

    def check_alive(self) -> bool:
        if self.health <= 0:
            self.health = 0
            return False
        else: return True

    def to_dict(self) -> dict:
        ...