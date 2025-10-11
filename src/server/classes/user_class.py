from .player import Player


class User:
    def __init__(self, id: int, hero: Player, status: bool=True):
        self.id = id
        self.hero = hero
        self.status = status