from typing import TYPE_CHECKING

from game.classes.entity.resistances import Resistances
from game.classes.items.damages import Damage
from game.classes.items.weapon import Weapon

from ..entity import Equipment
from .attributes import Attributes

if TYPE_CHECKING:
    from game.manager import AttackResult
    from ..entity import Entity


class Characteristics:
    """Класс для брони, урона, уклонения и тп"""
    def __init__(self, tracking_attributes: Attributes, tracking_equipment: Equipment, resistances: dict, base_hp: int = 20) -> None:
        self.tracking_attributes = tracking_attributes
        self.tracking_equipment = tracking_equipment
        self.resistances = Resistances(resistances)
        self.health: float = self.get_max_health(base_hp)

    def get_health(self) -> float:
        return self.health

    def get_max_health(self, base_hp: int=20) -> float:
        base_hp = base_hp
        hp_from_strength = self.tracking_attributes.get_health_from_strength()
        hp_equipment_buffes = self.tracking_equipment.get_health_buff()
        additional_hp = 0
        for stat, value in hp_equipment_buffes.items():
            if stat == "strength":
                additional_hp += value * Attributes.streng_hp_multiplicator
            elif stat == "max_health":
                additional_hp += value
        total_hp = base_hp + hp_from_strength + additional_hp
        return total_hp
    
    def get_weapon_damage(self) -> Damage:
        # weapon damage
        weapon = self.tracking_equipment.get_equip("mainhand")
        if not weapon: return Damage({})
        if isinstance(weapon, Weapon):
            return weapon.get_damage()
        else:
            return Damage({})
    
    def get_accuracy_rating(self) -> int:
        agility = self.tracking_attributes.get_agility() # 1 agility rating = 2 accuracy rating
        accuracy_rating = agility * 2
        return accuracy_rating

    def get_evasion_rating(self) -> int:
        # базовое уклонение зависит от процента уклонения на броне
        return self.tracking_equipment.get_evasion()
    
    def get_evasion_chance(self, enemy: "Entity") -> float:
        ...

    def get_armor_rating(self) -> int:
        # 10 armor rating absorbing 1% physical damage
        return self.tracking_equipment.get_armor()

    def take_damage(self, weapon: Weapon) -> "AttackResult":
        from game.manager import AttackResult
        from random import randint
        crit_status = False
        critical_chance = weapon.get_crit()
        critical_multy = weapon.get_crit_multy()
        rnd = randint(1, 101)
        if rnd <= critical_chance:
            crit_status = True
        physical_damage = weapon.get_damage().physical.get_value() * (critical_multy if crit_status else 1)
        fire_damage = weapon.get_damage().fire.get_value() * (critical_multy if crit_status else 1)
        cold_damage = weapon.get_damage().cold.get_value() * (critical_multy if crit_status else 1)
        lightning_damage = weapon.get_damage().lightning.get_value() * (critical_multy if crit_status else 1)
        reduced_physical_damage = physical_damage - (physical_damage * (self.get_armor_rating() / 10))
        reduced_fire_damage = fire_damage - (fire_damage / 100 * self.resistances.fire.get_value())
        reduced_cold_damage = cold_damage - (cold_damage / 100 * self.resistances.cold.get_value())
        reduced_lightning_damage = lightning_damage - (lightning_damage / 100 * self.resistances.lightning.get_value())
        self.health -= reduced_physical_damage
        self.health -= reduced_fire_damage
        self.health -= reduced_cold_damage
        self.health -= reduced_lightning_damage
        total_damage = reduced_physical_damage + reduced_fire_damage + reduced_cold_damage + reduced_lightning_damage
        attack_result = AttackResult(alive=self.check_alive(), damage=total_damage, crit=crit_status)
        return attack_result

    def check_alive(self) -> bool:
        if self.health <= 0:
            self.health = 0
            return False
        else: return True

    def to_dict(self) -> dict:
        ...