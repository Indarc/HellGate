from game import game_manager
from game.classes.items import Item

class TestItemManager:
    def test_items_load(self):
        item_dict = {
            "type": "consumable",
            "identificator": "apple",
            "rarity": "common",
            "cost": 5,
            "stacked": True,
            "description": "Apple from tree."
        }
        item = Item(data=item_dict)