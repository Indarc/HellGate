from types import NoneType
from typing import Optional


class Prefix:
    def __init__(self, stat: str, value: int) -> None:
        setattr(self, stat, value)

    def get_attribute(self) -> tuple[str | None, int | float | None]:
        # Получаем имя и значение первого атрибута
        for attr_name, attr_value in self.__dict__.items():
            return attr_name, attr_value
        return None, None  # Если атрибутов нет

class ArmorPrefix(Prefix):
    def __init__(self, stat: str, value: int) -> None:
        super().__init__(stat, value)
    

class WeaponPrefix(Prefix):
    def __init__(self, stat: str, value: int) -> None:
        super().__init__(stat, value)


class BagPrefix(Prefix):
    def __init__(self, stat: str, value: int) -> None:
        super().__init__(stat, value)
    