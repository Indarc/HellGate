import pytest

from game.classes.entity.player import Player
from game.classes.items import *
from game.classes.entity.characteristicts import Attributes
from game.classes.inventory.inventory import Inventory
from game.classes.items import weapon


def make_weapon(name: str = "Sword of Testing", damage: int = 10, equip_requirements: dict= {"level": 1}) -> Weapon:
    weapon_dict = {
        "item_type": "weapon",
        "id": 1,
        "name": name,
        "rare": "rare",
        "cost": 100,
        "description": "A sword used for testing purposes.",
        "emoji": "🗡️",
        "stacked": False,
        "stats": {
            "damage": damage,
            "crit": 5.0,
            "crit_multy": 2.0,
            "attack_speed": 1.0
        },
        "affixes": {
            "sufix": {
                "damage": 10,
                "crit": 5
            },
        "prefix": {
            "vitality": 10,
            "agility": 2
        }
        },
        "slot": "mainhand",
        "equip_requirements": equip_requirements
    }
    return Weapon(data=weapon_dict)

def make_armor():
    armor_dict = {
        "item_type": "armor",
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
                "max_health": 10
            },
            "suffixes": {
                
            }
        }
    }
    return Armor(data=armor_dict)


class TestEquipment:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.player = Player(name="TestPlayer")
        yield

    def test_equiping_from_inventory(self):
        weapon = make_weapon()
        self.player.inventory.add_item(weapon)
        assert self.player.equip_item(slot_id=0) is True
        assert self.player.equipment.mainhand == weapon
        assert self.player.inventory.slots[0].item == None
        assert self.player.inventory.slots[0].count == 0
        assert self.player.get_damage() == weapon.stats.damage
    
    def test_equiping_weapon(self):
        weapon = make_weapon()
        assert self.player.equip_item(item=weapon) is True
        assert self.player.equipment.mainhand == weapon
    
    def test_equiping_armor(self):
        armor = make_armor()
        assert self.player.equip_item(item=armor) is True
        assert self.player.equipment.body == armor

    def test2_equiping(self):
        # Тест замены оружия, если в экипировке уже есть оружие, то оно должно переместиться в инвентарь, а новое оружие должно стать экипированным
        weapon = make_weapon()
        self.player.inventory.add_item(weapon)
        self.player.equip_item(slot_id=0)
        second_weapon = make_weapon(name="Axe of Testing", damage=15)
        self.player.inventory.add_item(second_weapon)
        self.player.equip_item(slot_id=0)
        assert self.player.equipment.mainhand == second_weapon
        assert self.player.inventory.slots[0].item == weapon

        # TODO test equipping item with invalid type, for example, potion or something else
        # TODO тест экипировки оружия при полном инвентаре, если в инвентаре нет свободного места для перемещения экипированного оружия, то экипировка нового оружия должна быть невозможна

    def test_unequiping(self):
        weapon = make_weapon()
        self.player.equip_item(weapon)
        assert self.player.unequip_item("mainhand") is True
        assert self.player.equipment.mainhand == None
        assert self.player.inventory.slots[0].item == weapon
    