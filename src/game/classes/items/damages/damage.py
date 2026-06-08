from .cold_dmg import ColdDamage
from .fire_dmg import FireDamage
from .lightning_dmg import LightningDamage
from .physical_dmg import PhysicalDamage


class Damage:
    def __init__(self, data: dict[str, int]) -> None:
        self.physical = PhysicalDamage(data.get("physical", 0))
        self.fire = FireDamage(data.get("fire", 0))
        self.cold = ColdDamage(data.get("cold", 0))
        self.lightning = LightningDamage(data.get("lightning", 0))
    
    def to_dict(self) -> dict:
        return {
            "physical": self.physical.get_value(),
            "fire": self.fire.get_value(),
            "cold": self.cold.get_value(),
            "lightning": self.lightning.get_value()
        }