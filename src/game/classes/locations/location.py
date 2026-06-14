from .zone import Zone

from game.classes.entity import Player


class Location:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.players: dict[str, Player] = {} # { id[str]: player[Player] }
        self.zones: dict[str, Zone] = {}