from .player import Player


class User:
    def __init__(self, id: int, hero: Player, status: bool=True):
        self.id = id
        self.hero = hero
        # self.status = status
    
    def to_dict(self) -> dict:
        return {
            "_": "User",
            "id": self.id,
            "hero": self.hero.to_dict()
            # "status": self.status
        }