from .location import Location


class Forest(Location):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.identificator = "forest"
        