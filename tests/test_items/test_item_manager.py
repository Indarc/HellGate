from game import game_manager


class TestItemManager:
    def test_items_load(self):
        assert len(game_manager.item_manager.items) != 0