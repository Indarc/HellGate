from .entity import Entity


class Enemy(Entity):
    def __init__(self, name: str = None, level: int = 1, data: dict = None):
        super().__init__(name, level, data)