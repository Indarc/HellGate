from .item import Item


class Weapon(Item):
    """Class for weapon items"""
    def __init__(self, id: int=None, data: dict=None):
        super().__init__(id, data=data)
        if data:
            self.damage = data.get("damage")
            self.accuracy = data.get("accuracy")
            self.slot = data.get("slot")
            self.upgrade = data.get("upgrade")
        else:
            self.damage = self.item_dict.get("damage")
            self.accuracy = self.item_dict.get("accuracy")
            self.slot = self.item_dict.get("slot")
            self.upgrade = self.item_dict.get("upgrade")
    
    def get_damage(self) -> int:
        return self.damage
    
    def get_accuracy(self) -> int:
        return self.accuracy
    
    def to_dict(self) -> dict:
        item_dict = super().to_dict()
        item_dict.update("_", "weapon")
        weapon_dict = {
            "damage": self.damage,
            "accuracy": self.accuracy,
            "slot": self.slot,
            "upgrade": self.upgrade
        }
        return item_dict + weapon_dict