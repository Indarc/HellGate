import pytest

from game.classes.entity import Player


def test_make_weapon():
    weapon_dict = {
    "item_type": "weapon",
    "id": 0,
    "name": "Ржавый меч",
    "rare": "common",
    "cost": 0.0,
    "description": "Старый и ржавый меч, который не может нанести серьезного урона. Его можно найти в заброшенных местах или у побежденных врагов.",
    "stacked": False,
    "stats": {
        "damage": 2.0,
        "crit": 0.0,
        "crit_multy": 1.5,
        "attack_speed": 1,
        "upgrade": 2
    },
    "affixes": {
        "sufix": {
            "damage": 2.0
        },
        "prefix": {
            "vitality": 10
        }
    },
    "slot": "mainhand",
    "emoji": "🗡️",
    "equip_requirements": {
        "level": 1
    }
}

def test_make_armor():
    ...

def test_make_bag():
    ...
