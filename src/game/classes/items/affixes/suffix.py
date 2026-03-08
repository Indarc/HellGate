class Suffix:
    def __init__(self, suffix: tuple[str, int | float]) -> None:
        setattr(self, suffix[0], suffix[1])
    
    def get_attribute(self) -> tuple[str | None, int | float | None]:
        # Получаем имя и значение первого атрибута
        for attr_name, attr_value in self.__dict__.items():
            return attr_name, attr_value
        return None, None  # Если атрибутов нет


class ArmorSuffix(Suffix):
    def __init__(self, suffix: tuple[str, int | float]) -> None:
        super().__init__(suffix)
    

class WeaponSuffix(Suffix):
    def __init__(self, suffix: tuple[str, int | float]) -> None:
        super().__init__(suffix)


class BagSuffix(Suffix):
    def __init__(self, suffix: tuple[str, int | float]) -> None:
        super().__init__(suffix)