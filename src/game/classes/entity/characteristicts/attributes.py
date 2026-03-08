
from typing import Optional

from server.config import loggers



class ReturnAttributes:
    def __init__(self, agility: int=3, strength: int=3, intelligence: int=3, data: Optional[dict]=None):
        self.agility: int = data.get("agility", 0) if data else agility
        self.strength: int = data.get("strength", 0) if data else strength
        self.intelligence: int = data.get("intelligence", 0) if data else intelligence
        self.upgrade_points: int = data.get("upgrade_points", 0) if data else 0
    
    def get_agility(self):
        return self.agility
    
    def get_strength(self):
        return self.strength
    
    def get_intelligence(self):
        return self.intelligence

class Attributes(ReturnAttributes):
    streng_hp_multiplicator = 5
    def __init__(self, agility: int=3, strength: int=3, intelligence: int=3, data: Optional[dict]=None):
        super().__init__(agility, strength, intelligence, data)
    
    def get_health_from_strength(self) -> float:
        return (self.strength * __class__.streng_hp_multiplicator) # default 15

    def add_attributes(self, agility: int=0, strength: int=0, intelligence: int=0):
        """Update stats with given values. If value is not given, it will not be changed."""
        self.agility += agility
        self.strength += strength
        self.intelligence += intelligence

    def add_upgrade_points(self, value: int):
        self.upgrade_points += value

    def to_dict(self) -> dict:
        return {
            "_": "Attributes",
            "agility": self.agility,
            "strength": self.strength,
            "intelligence": self.intelligence,
            "upgrade_points": self.upgrade_points
        }

