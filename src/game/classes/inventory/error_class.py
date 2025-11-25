# Base inventory errors
class DontEnoughSlotsError:
    def __init__(self, message: str="У вас кончились слоты в инвентаре"):
        self.message = message

class ItemRemoveError:
    def __init__(self, message: str="Can`t delete item from inventory"):
        self.message = message