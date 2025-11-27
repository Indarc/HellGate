from server.loggers import Loggers

from game.classes.items import *


class Outfit:
    def __init__(self, data: dict=None):
        if data:
            self.main_weapon: Weapon = Weapon(data.get("main_weapon")) if data.get("main_weapon") else None
            self.offhand_weapon: Weapon = None
            self.helmet: dict = None
            self.armor: dict = None
            self.boots: dict = None
            self.gloves: dict = None
            self.belt: dict = None
            self.ring1: dict = None
            self.ring2: dict = None
            self.amulet: dict = None
            self.bag: dict = None
        else:
            self.main_weapon: Weapon = None
            self.offhand_weapon: Weapon = None
            self.helmet: dict = None
            self.armor: dict = None
            self.boots: dict = None
            self.gloves: dict = None
            self.belt: dict = None
            self.ring1: dict = None
            self.ring2: dict = None
            self.amulet: dict = None
            self.bag: dict = None
    
    def calculate_stats(self):
        ...
    
    def to_dict(self) -> dict:
        """Return dictionary with equiped items

        Returns :
            dict: {item_slot (str), item_id (int) / None}
        """
        return {
            "main_weapon": self.main_weapon.to_dict() if isinstance(self.main_weapon, Weapon) else None,
            "offhand_weapon": None,
            "helmet": None,
            "armor": None,
            "boots": None,
            "gloves": None,
            "belt": None,
            "ring1": None,
            "ring2": None,
            "amulet": None,
            "bag": None
        }

class Stats:
    def __init__(self, tracking_outfit: Outfit ,stamina: int=5, power: int=5, agility: int=3, strength: int=3, intelligence: int=3, accuracy: int=1, data: dict=None):
        if data:
            t = data.get("_")
            if t != "Stats":
                Loggers.game_classes.error(f"[STATS_INIT] Not supported dict to initialization Stats object: {t}")
                return
            self.tracking_outfit = tracking_outfit
            self.stamina = data.get("stamina")
            self.power = data.get("power")
            self.agility = data.get("agility")
            self.strength = data.get("strength")
            self.intelligence = data.get("intelligence")
            self.accuracy = data.get("accuracy")
        else:
            self.tracking_outfit = tracking_outfit
            self.stamina = stamina
            self.power = power
            self.agility = agility
            self.strength = strength
            self.intelligence = intelligence
            self.accuracy = accuracy
            self.outfit = Outfit()
    
    def health(self) -> int:
        return (self.stamina * 8) + (self.strength * 2) # default 46hp
    
    def damage(self) -> int:
        return self.power

    def evasion(self) -> int:
        # maximum evasion 100% to monsters and 85 to players
        # 1 evasion rating = 0.1% chance to avoid attack
        clear_evasion = self.agility * 0.1
        if clear_evasion > 75:
            evasion = 75
        else:
            evasion = clear_evasion
        return int(evasion)

    def hit_chance(self) -> int:
        # default hit_chance = 45%, maximum hit chance 100%
        # 1 accuracy rating = 0.2% hit chance
        hit = 45
        hit += self.accuracy * 0.2
        if hit > 100:
            hit = 100
        return hit

    def add_stat(self, stamina: int=0, power: int=0, agility: int=0, strength: int=0, intelligence: int=0, accuracy: int=0):
        self.stamina += stamina
        self.power += power
        self.agility += agility
        self.strength += strength
        self.intelligence += intelligence
        self.accuracy += accuracy
        
    def to_dict(self) -> dict:
        return {
            "_": "Stats",
            "stamina": self.stamina,
            "power": self.power,
            "agility": self.agility,
            "strength": self.strength,
            "intelligence": self.intelligence,
            "accuracy": self.accuracy
        }


class Level:
    def __init__(self, tracking_stats: Stats, level: int=1, experience: int = 0, data: dict=None):
        if data:
            t = data.get("_")
            if t != "Level":
                Loggers.game_classes.error(f"[LEVEL_INIT] Not supported dict to initialization Level object: {t}")
                return
            
            self.tracking_stats = tracking_stats
            self.level = data.get("level")
            self.experience = data.get("experience")
            self.max_experience = data.get("max_experience")
        else:
            self.tracking_stats = tracking_stats
            self.level = level
            self.experience = experience
            self.max_experience = self.level * 10
        
    def get_level(self) -> int:
        return self.level
    
    def get_experience(self) -> tuple[int, int]:
        return (self.experience, self.max_experience)

    def lvl_up(self):
        # remnant = self.max_experience - self.experience
        self.level += 1
        self.experience = (self.experience - self.max_experience) if self.experience >= self.max_experience else 0 # to absorb error with extra lvl_up
        self.max_experience = self.level * 10
        self.tracking_stats.add_stat(stamina=1, power=1)

        # TODO: message to user about level up

        if self.experience >= self.max_experience:
            self.lvl_up()

    def add_exp(self, exp):
        self.experience += exp
        if self.experience >= self.max_experience:
            self.lvl_up()
    
    def to_dict(self) -> dict:
        return {
            "_": "Level",
            "tracking_stats": self.tracking_stats.to_dict(),
            "level": self.level,
            "experience": self.experience,
            "max_experience": self.max_experience
        }

class AtackResult:
    def __init__(self, alive: bool=True):
        self.alive = alive

class Entity:
    def __init__(self, name: str = None, level: int=1, data: dict = None):
        if data:
            t = data.get("_")
            if t != "Player":
                Loggers.game_classes.error(f"[ENTITY_INIT] Not supported dict to initialization Entity object: {t}")
                return
            self.name = data.get("name")
            self.outfit = Outfit(data=data.get("outfit"))
            self.stats = Stats(tracking_outfit=self.outfit, data=data.get("stats"))
            self.level = Level(data=data.get("level"), tracking_stats=self.stats)
            self.health = data.get("health")
            self.armor = data.get("armor")
        else:
            if not name or not level:
                Loggers.game_classes.error("[ENTITY_INIT] Entity object requered paramateres to initializating")
                return
            
            self.name = name
            self.outfit = Outfit()
            self.stats = Stats(tracking_outfit=self.outfit)
            self.level = Level(self.stats)
            self.health = self.max_health()
            self.armor = 0

    def damage(self) -> int:
        return self.stats.damage()
    
    def max_health(self) -> int:
        return self.stats.health()
    
    def evasion(self) -> int:
        return self.stats.evasion()
    
    def get_experience(self, exp: int):
        self.level.add_exp(exp)
    
    def atack(self, target: "Entity"):
        # TODO: crit and more
        atack_result = target.take_damage(self.damage())

    def take_damage(self, dmg: int) -> AtackResult:
        # TODO: evasion chance
        # TODO: armor
        self.health -= dmg
        return AtackResult(self.check_alive())

    def check_alive(self) -> bool:
        if self.health <= 0:
            return False
        else:
            return True
    
    def battle_banner(self) -> str:
        text = f"""
❤️HP: {self.health}/{self.max_health()}
Имя: {self.name}
Уровень: {self.level.get_level()}

⚔️Урон: {self.damage()}
🛡️Броня: {self.armor}
👟Уклонение: {self.evasion()}%
🎯Точность: {self.stats.accuracy}%
"""
        return text