import pytest

from game.classes.entity.player import Player
from game.classes.items import Item


class TestInventoryActions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.player = Player(name="TestPlayer")
        yield

    def create_item(self, name: str = "Test Item", item_type: str = "weapon") -> Item:
        item_dict = {
            "item_type": item_type,
            "id": 1,
            "name": name,
            "rare": "common",
            "cost": 10,
            "description": "A test item.",
            "emoji": "🧪",
            "stacked": False
        }
        return Item(data=item_dict)
    
    def create_stacked_item(self, name: str = "Test Stacked Item", item_type: str = "another") -> Item:
        item_dict = {
            "item_type": item_type,
            "id": 2,
            "name": name,
            "rare": "common",
            "cost": 5,
            "description": "A test stacked item.",
            "emoji": "🍎",
            "stacked": True
        }
        return Item(data=item_dict)

    def test_add_item(self):
        item = self.create_item()
        self.player.inventory.add_item(item)
        assert self.player.inventory.slots[0].item == item
        assert self.player.inventory.slots[0].count == 1
    
    def test_add_stacked_item(self):
        item = self.create_stacked_item()
        self.player.inventory.add_item(item)
        assert self.player.inventory.slots[0].item == item
        assert self.player.inventory.slots[0].count == 1
        self.player.inventory.add_item(item)
        assert self.player.inventory.slots[0].item == item
        assert self.player.inventory.slots[0].count == 2

    def test_inventory_full(self):
        item = self.create_item()
        for i in range(self.player.inventory.max_space):
            self.player.inventory.add_item(item)
        with pytest.raises(Exception) as excinfo:
            self.player.inventory.add_item(item)
        assert "DontEnoughSlotsError" in str(excinfo.type)
    
    def test_extract_item(self):
        item = self.create_item()
        self.player.inventory.add_item(item)
        extracted_item = self.player.inventory.extract_item(0)
        assert extracted_item is not None
        assert extracted_item[0] == item
        assert extracted_item[1] == 1
        assert self.player.inventory.slots[0].item is None
        assert self.player.inventory.slots[0].count == 0
    
    def test_slot_overload(self):
        item = self.create_stacked_item()
        with pytest.raises(Exception) as excinfo:
            for _ in range(100):
                self.player.inventory.add_item(item)
        assert "SlotOverloadError" in str(excinfo.type)
    
    def test2_slot_overload(self):
        item = self.create_stacked_item()
        self.player.inventory.add_item(item, count=99)
        with pytest.raises(Exception) as excinfo:
            self.player.inventory.add_item(item)
        assert "SlotOverloadError" in str(excinfo.type)