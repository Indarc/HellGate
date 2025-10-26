# Base inventory errors
class DontEnoughSpaceError:
    def __init__(self, message: str="Don`t enough space in inventory"):
        self.message = message

class ItemRemoveError:
    def __init__(self, message: str="Can`t delete item from inventory"):
        self.message = message