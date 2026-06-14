from email.mime import base

import pytest

from game.classes.entity import Player
from game.classes.entity.characteristicts import Attributes
from game.classes.items import Armor


def create_armor():
    armor_dict = {
        "type": "armor",
        "id": 2,
        "name": "Test Armor",
        "rare": "common",
        "cost": 0.0,
        "description": "Armor for testing",
        "stacked": False,
        "slot": "body",
        "emoji": "👘",
        "stats": {
            "armor": 1,
            "evasion": 10,
            "upgrade": 0
        },
        "equip_requirements": {
            "level": 1
        },
        "affixes":{
            "prefixes": {
                "max_health": 10,
                "strength": 5
            },
            "suffixes": {
                
            }
        }
    }
    return Armor(armor_dict)


class TestCharacteristics:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.player = Player(name="TestPlayer")
        yield

    def test_armor_stats(self):
        armor = create_armor()
        self.player.equip_item(armor)

        assert self.player.get_armor_rating() == armor.stats.get_armor_rating()
        assert self.player.get_evasion_rating() == armor.stats.get_evasion_rating()

    def test_armor_affixes(self):
        armor = create_armor()
        base_hp = self.player.get_max_health()
        self.player.equip_item(armor)

        new_hp = self.player.get_max_health()
        assert new_hp > base_hp