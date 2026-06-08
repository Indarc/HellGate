from game.classes.items.item import EquipItem


class Bag(EquipItem):
    def __init__(self, data: dict):
        super().__init__(data)
        self.space = data.get("space", 0)
        self.equip_requirements = data.get("equip_requirements", {})
    
    def to_dict(self) -> dict:
        item_dict = super().to_dict()
        item_dict.update({
            "space": self.space,
            "equip_requirements": self.equip_requirements
        })
        return item_dict