# Base inventory errors
class DontEnoughSpaceError:
    def __init__(self, message: str="dont enough space in inventory"):
        self.message = message