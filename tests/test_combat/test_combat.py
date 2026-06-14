import pytest

from game.classes.entity import Entity
from game import game_manager
from game.classes.items import Weapon, Armor


def make_weapon(physical: int = 0, fire: int = 0, cold: int = 0, lightning: int = 0, crit_chance: float = 0.0):
    weapon_dict = {
        "type": "weapon",
        "id": 4,
        "name": "Огненный меч",
        "rare": "magic",
        "cost": 0.0,
        "description": "Старый и ржавый меч, который не может нанести серьезного урона. Его можно найти в заброшенных местах или у побежденных врагов.",
        "stacked": False,
        "stats": {
            "damage": {
                "physical": physical,
                "fire": fire,
                "cold": cold,
                "lightning": lightning
            },
            "crit": crit_chance,
            "crit_multy": 2,
            "attack_speed": 2,
            "attribute_scale": ["strength", 2],
            "upgrade": 0   
        },
        "slot": "mainhand",
        "emoji": "🗡️",
        "equip_requirements": {
            "level": 1
        }
    }
    return Weapon(weapon_dict)

def make_armor(armor: int=0, evasion: int=0):
    armor_dict = {
        "type": "armor",
        "id": 2,
        "name": "Грязная накидка",
        "rare": "common",
        "cost": 0.0,
        "description": "Старая накидка, вся пропитанная грязью. Не особо защитит от врагов.",
        "stacked": False,
        "slot": "body",
        "emoji": "👘",
        "stats": {
            "armor": armor,
            "evasion": evasion
        },
        "equip_requirements": {
            "level": 1
        }
    }
    return Armor(armor_dict)


class TestCombat:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.entity_one = Entity(name="Entity_One")
        self.entity_two = Entity(name="Entity_Two")
        self.combat_manager = game_manager.combat_manager
    
    def test_physical_atack(self):
        weapon = make_weapon(physical=10)
        self.entity_one.equip_item(weapon)
        start_hp = self.entity_two.get_health()
        attack_result = self.combat_manager.atack(attacker=self.entity_one, target=self.entity_two)
        assert self.entity_two.get_health() == start_hp - attack_result.damage
    
    def test_physical_damage_reduction(self):
        weapon = make_weapon(physical=10)
        self.entity_one.equip_item(weapon)
        armor = make_armor(armor=15)
        self.entity_two.equip_item(armor)
        start_hp = self.entity_two.get_health()
        attack_result = self.combat_manager.atack(attacker=self.entity_one, target=self.entity_two)
        assert self.entity_two.get_health() == start_hp - attack_result.damage

    def test_fire_atack(self):
        weapon = make_weapon(fire=10)
        self.entity_one.equip_item(weapon)
        self.entity_two.characteristics.resistances.fire.value = 25 # set fire resistance 25%
        start_hp = self.entity_two.get_health()
        attack_result = self.combat_manager.atack(attacker=self.entity_one, target=self.entity_two)
        assert self.entity_two.get_health() == start_hp - attack_result.damage
    
    def test_crit_atack(self):
        weapon = make_weapon(physical=10, crit_chance=100)
        self.entity_one.equip_item(weapon)
        start_hp = self.entity_two.get_health()
        attack_result = self.combat_manager.atack(attacker=self.entity_one, target=self.entity_two)
        assert self.entity_two.get_health() == start_hp - attack_result.damage
    
    def test_evasion_chance(self):
        weapon = make_weapon(physical=10)
        self.entity_one.equip_item(weapon)
        self.entity_two.characteristics.tracking_attributes.agility = 10
        attack_result = self.entity_one.attack(self.entity_two)
        assert attack_result.evaded == True

        armor = make_armor(evasion=100)
        self.entity_two.equip_item(armor)
        attack_result = self.entity_one.attack(self.entity_two)
        assert attack_result.evaded == False