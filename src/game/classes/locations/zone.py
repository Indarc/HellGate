from game.classes.entity import Enemy


class Zone():
    """Base class for location`s zones"""
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.enemy_list: list[Enemy] = []
        self.search_time = 1