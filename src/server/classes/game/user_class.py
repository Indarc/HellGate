from .player import Player
from server.classes.game.player import Player

from server.classes.game.logger import logger


class User:
    def __init__(self, id: int=None, hero: Player=None, status: bool=True, data=None):
        if data:
            ...
        else:
            if not id or not hero:
                logger.error("")
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