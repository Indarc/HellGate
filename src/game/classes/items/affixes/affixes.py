from random import randint
from typing import Optional

from .suffix import Suffix
from .prefix import Prefix


class Affixes:
    def __init__(self, affixes: Optional[dict]=None, item_rarity: str="common") -> None:
        if item_rarity == "magic":
            self.max_affixes = 2
        elif item_rarity == "rare":
            self.max_affixes = 3
        elif item_rarity == "unic":
            self.max_affixes = 3
        else:
            self.max_affixes = 1
        if not affixes:
            return
        prefixes_dict: dict = affixes.get("prefixes", {})
        suffixes_dict: dict = affixes.get("suffixes", {})
        prefixes = [Prefix(x, y) for x, y in prefixes_dict.items()]
        suffixes = [Suffix(x, y) for x, y in suffixes_dict.items()]
        self.prefixes = []
        self.suffixes = []
        for i in range(self.max_affixes):
            try:
                self.prefixes.append(prefixes.pop(0))
            except IndexError:
                pass
            try:
                self.suffixes.append(suffixes.pop(0))
            except IndexError:
                pass
    
    def get_buffes(self) -> dict[str, dict[str, int]]:
        buffes = {
            "max_health": {},
            "protections": {},
            "resistances": {}
        }
        for prefix in self.prefixes:
            attr, value = prefix.get_attribute()
            if attr in ["strength", "max_health"]:
                buffes["max_health"].update({attr: value})
            if attr in ["armor", "evasion"]:
                buffes["protections"].update({attr: value})
        for suffix in self.suffixes:
            attr, value = suffix.get_attribute()
            if attr in ["fire_resistance", "cold_resistance", "lighting_resistance"]:
                buffes["resistances"].update({attr: value})

        return buffes

    def get_prefixes(self) -> list[Prefix]:
        return self.prefixes
    
    def get_suffixes(self) -> list[Suffix]:
        return self.suffixes
    
    def add_sufix(self) -> bool:
        ...
    
    def add_prefix(self) -> bool:
        ...
    
    def to_dict(self) -> dict:
        ...