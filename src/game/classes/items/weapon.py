from .item import Item


class Weapon(Item):
    """Class for weapon items"""
    def __init__(self, id: int=None, data: dict=None):
        super().__init__(id, data=data)
        if data:
            self.damage: int = data.get("damage")
            self.accuracy: float = data.get("accuracy")
            self.slot: str = data.get("slot") # main hand / off hand
            self.upgrade: int = data.get("upgrade")
            self.crit: float = data.get("crit")
        else:
            self.damage: int = self.item_dict.get("damage")
            self.accuracy: float = self.item_dict.get("accuracy")
            self.slot: str = self.item_dict.get("slot") # main hand / off hand
            self.upgrade: int = self.item_dict.get("upgrade")
            self.crit: float = self.item_dict.get("crit")
    
    def get_damage(self) -> int:
        return self.damage
    
    def get_accuracy(self) -> float:
        return self.accuracy
    
    def get_crit(self) -> float:
        return self.crit

    def to_dict(self) -> dict:
        item_dict = super().to_dict()
        item_dict.update(_="weapon")
        weapon_dict = {
            "damage": self.damage,
            "crit": self.crit,
            "accuracy": self.accuracy,
            "slot": self.slot, # main hand / off hand
            "upgrade": self.upgrade
        }
        item_dict.update(weapon_dict)
        return item_dict