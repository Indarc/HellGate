
from .attributes import Attributes
from server.config import loggers


class Level:
    def __init__(self, tracking_attributes: Attributes, level: int=1, experience: int = 0, data: dict | None=None):
        self.tracking_attributes = tracking_attributes
        self.level: int = data.get("level", 1) if data else level
        self.experience: int = data.get("experience", 0) if data else experience
        self.max_experience: int = data.get("max_experience", self.level * 10) if data else self.level * 10
        
    def get_level(self) -> int:
        return self.level
    
    def get_experience(self) -> tuple[int, int]:
        return (self.experience, self.max_experience)

    def lvl_up(self):
        # remnant = self.max_experience - self.experience
        self.level += 1
        self.experience = (self.experience - self.max_experience) if self.experience >= self.max_experience else self.experience # to absorb error with extra lvl_up
        self.max_experience = self.level * 10
        self.tracking_attributes.add_upgrade_points(3)

        # TODO: message to user about level up and 3 free upgrade attributes points

        if self.experience >= self.max_experience:
            self.lvl_up()

    def add_exp(self, exp) -> None:
        self.experience += exp
        if self.experience >= self.max_experience:
            self.lvl_up()
    
    def to_dict(self) -> dict:
        return {
            "_": "Level",
            "level": self.level,
            "experience": self.experience,
            "max_experience": self.max_experience
        }

