from .item import EquipItem, EquipItemStats


class Armor(EquipItem):
    def __init__(self, data: dict):
        super().__init__(data)
        self.stats = ArmorStats(data.get("stats", {}))


class ArmorStats(EquipItemStats):
    def __init__(self, stats: dict) -> None:
        super().__init__(stats)
        self.armor: int = stats.get("armor", 0)
        self.evasion: int = stats.get("evasion", 0)
    
    def get_armor(self) -> int:
        return self.armor
    
    def get_evasion(self) -> int:
        return self.evasion