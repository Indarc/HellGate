from typing import Optional

from .item import EquipItem, EquipItemStats
from .damages import Damage


class Weapon(EquipItem):
    """Class for weapon items"""
    def __init__(self, data: dict):
        super().__init__(data=data)
        self.stats = WeaponStats(data.get("stats", {}))
    
    def banner(self, count: int):
        text = super().banner(count=count)
        slot_item = "Основной" if self.slot == 0 else "Вспомогательное"
        text += f"""
----------------------------------
Урон: {self.get_damage()} ❣️
Крит. шанс: {self.get_crit()}%
Множитель критического урона: x{self.get_crit_multy()}
Скорость атака: {self.get_attack_speed()}
Слот оружия: {slot_item}
"""
        return text

    def get_damage(self) -> Damage:
        weapon_damage: Damage = self.stats.damage
        # TODO учитывать аффиксы при выдачи общего урона
        return weapon_damage
    
    def get_crit(self) -> float:
        weapon_crit: Optional[float] = getattr(self.stats, "crit", None)
        if not weapon_crit:
            return 0.0
        # TODO учитывать аффиксы при выдачи общего крита
        return weapon_crit

    def get_crit_multy(self) -> float:
        weapon_crit_multy: Optional[float] = getattr(self.stats, "crit_multy", None)
        if not weapon_crit_multy:
            return 0.0
        return weapon_crit_multy

    def get_attack_speed(self) -> float:
        weapon_attack_speed: Optional[float] = getattr(self.stats, "attack_speed", None)
        if not weapon_attack_speed:
            return 0.0
        return weapon_attack_speed

    def to_dict(self) -> dict:
        item_dict = super().to_dict()
        item_dict.update(_="weapon")
        weapon_dict = {
            "stats":self.stats.to_dict(),
            "slot": self.slot, # main hand / off hand
        }
        item_dict.update(weapon_dict)
        return item_dict


class WeaponStats(EquipItemStats):
    def __init__(self, stats: dict):
        super().__init__(stats)
        self.damage = Damage(stats.get("damages", {}))
        self.crit: float = stats.get("crit", 0.0)
        self.crit_multy: float = stats.get("crit_multy", 0.0)
        self.attack_speed: float = stats.get("attack_speed", 0.0)
    
    def to_dict(self):
        return {
            "damage": self.damage.to_dict(),
            "crit": self.crit,
            "crit_multy": self.crit_multy,
            "attack_speed": self.attack_speed
        }