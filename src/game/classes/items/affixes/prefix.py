from types import NoneType
from typing import Optional


class Prefix:
    def __init__(self, prefix: tuple[str, int | float]) -> None:
        setattr(self, prefix[0], prefix[1])

    def get_attribute(self) -> tuple[str | None, int | float | None]:
        # Получаем имя и значение первого атрибута
        for attr_name, attr_value in self.__dict__.items():
            return attr_name, attr_value
        return None, None  # Если атрибутов нет

class ArmorPrefix(Prefix):
    def __init__(self, prefix: tuple[str, int | float]) -> None:
        super().__init__(prefix)
    

class WeaponPrefix(Prefix):
    def __init__(self, prefix: tuple[str, int | float]) -> None:
        super().__init__(prefix)


class BagPrefix(Prefix):
    def __init__(self, prefix: tuple[str, int | float]) -> None:
        super().__init__(prefix)
    