from typing import Optional

from .cold_dmg import ColdDamage
from .fire_dmg import FireDamage
from .lightning_dmg import LightningDamage
from .physical_dmg import PhysicalDamage


class Damage:
    def __init__(self, data: Optional[dict[str, int]]=None) -> None:
        self.physical = PhysicalDamage(data.get("physical", 0)) if data else PhysicalDamage(0)
        self.fire = FireDamage(data.get("fire", 0)) if data else FireDamage(0)
        self.cold = ColdDamage(data.get("cold", 0)) if data else ColdDamage(0)
        self.lightning = LightningDamage(data.get("lightning", 0)) if data else LightningDamage(0)
    
    def interface(self) -> str:
        return f"❣️{self.physical.get_value()} 🔥{self.fire.get_value()} ❄️{self.cold.get_value()} ⚡️{self.lightning.get_value()}"

    def to_dict(self) -> dict:
        return {
            "physical": self.physical.get_value(),
            "fire": self.fire.get_value(),
            "cold": self.cold.get_value(),
            "lightning": self.lightning.get_value()
        }