# Base inventory errors
class DontEnoughSlotsError(Exception):
    def __init__(self, message: str="У вас кончились слоты в инвентаре"):
        self.type = "DontEnoughSlotsError"
        self.value = message
        super().__init__(self.value, self.type)

class ItemRemoveError(Exception):
    def __init__(self, message: str="Не удалось удалить предмет из инвентаря"):
        self.type = "ItemRemoveError"
        self.value = message
        super().__init__(self.value, self.type)

class SlotOverloadError(Exception):
    def __init__(self, message: str="Вы пытаетесь положить слишком много предметов в один слот"):
        self.type = "SlotOverloadError"
        self.value = message
        super().__init__(self.value, self.type)