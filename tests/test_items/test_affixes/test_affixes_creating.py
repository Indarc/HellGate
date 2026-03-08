from game.classes.items.affixes import Affixes



def test_affixes_creating():
    affixes_dict = {
        "prefixes": {
            "armor": 10,
            "evasion": 5
        },
        "suffixes": {
            "cold_resistance": 10
        }
    }
    affixes = Affixes(affixes_dict, item_rarity="magic")
    assert affixes.max_affixes == 2
    assert getattr(affixes.prefixes[0], "armor") is not None
    affixes = Affixes(affixes_dict, item_rarity="rare")
    assert affixes.max_affixes == 3
    assert affixes.prefixes[0].get_attribute()[0] == "armor"
    assert affixes.prefixes[0].get_attribute()[1] == 10


def test_empty_affixes():
    affixes_dict = {"prefixes": {},"suffixes": {}}

    affixes = Affixes(affixes_dict, item_rarity="common")
    assert len(affixes.prefixes) == 0
    assert len(affixes.suffixes) == 0


def test_overload_affixes():
    affixes_dict = {
        "prefixes": {
            "armor": 10,
            "evasion": 5,
            "max_health": 100,
            "armor%": 100
        },
        "suffixes": {
            "cold_resistance": 10,
            "fire_resistance": 10,
            "lightning_resistance": 10,
            "poison_resistance": 10,
        }
    }
    affixes = Affixes(affixes_dict, item_rarity="magic")
    assert len(affixes.get_prefixes()) == 2
    assert len(affixes.get_suffixes()) == 2
