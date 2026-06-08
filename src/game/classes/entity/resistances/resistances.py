from .fire_resistance import FireResistance
from .cold_resistance import ColdResistance
from .lighting_resistance import LightningResistance


class Resistances:
    def __init__(self, data: dict) -> None:
        self.fire = FireResistance(data.get("fire", 0))
        self.cold = ColdResistance(data.get("cold", 0))
        self.lightning = LightningResistance(data.get("lightning", 0))

    def to_dict(self) -> dict:
        return {
            "fire": self.fire.get_value(),
            "cold": self.cold.get_value(),
            "lightning": self.lightning.get_value()
        }