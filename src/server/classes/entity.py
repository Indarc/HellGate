class Stats:
    def __init__(self, stamina: int=5, power: int=5, agility: int=3, strength: int=3, intelligence: int=3, accuracy: int=1):
        self.stamina = stamina
        self.power = power
        self.agility = agility
        self.strength = strength
        self.intelligence = intelligence
        self.accuracy = accuracy
    
    def health(self) -> int:
        return (self.stamina * 8) + (self.strength * 2)
    
    def damage(self) -> int:
        return self.power

    def evasion(self) -> int:
        # maximum evasion 75%
        clear_evasion = self.agility * 0.5
        if clear_evasion > 75:
            evasion = 75
        else:
            evasion = clear_evasion
        return evasion

class Level:
    def __init__(self, level: int=1, experience: int = 0):
        self.level = level
        self.experience = experience
        self.max_experience = self.level * 10
    
    def get_level(self) -> int:
        return self.level
    
    def get_experience(self) -> tuple[int, int]:
        return (self.experience, self.max_experience)

    def lvl_up(self):
        remnant = self.max_experience - self.experience
        self.level += 1
        self.experience = remnant
        self.max_experience = self.level * 10

        # TODO: message to user about level up

    def add_exp(self, exp):
        self.experience += exp
        if self.experience >= self.max_experience:
            self.lvl_up()

class Entity:
    def __init__(self, name: str):
        self.name = name
        self.level = Level()
        self.stats = Stats()
        self.health = self.max_health()
        self.armor = 0
    
    def banner(self) -> str:
        exp = self.level.get_experience()
        text = f"""
❤️HP: {self.health}/{self.max_health()}
⚔️Урон: {self.damage()}
🛡️Броня: {self.armor}
Никнейм: {self.name}
Уровень: {self.level.get_level()}
Exp: {exp[0]}/{exp[1]}

Атрибуты:
🫀Выносливость: {self.stats.stamina}
💪Сила: {self.stats.power}
🤲Ловкость: {self.stats.agility}
🧠Интелект: {self.stats.intelligence}
🎯Точность: {self.stats.accuracy}
"""
    
    def damage(self) -> int:
        return self.stats.damage()
    
    def max_health(self) -> int:
        return self.stats.health()
    
    def evasion(self) -> int:
        return self.stats.evasion
    
    def get_experience(self, exp: int):
        self.level.add_exp(exp)
    
    def atack(self, target: "Entity"):
        # TODO: armor
        target.take_damage(self.damage)

    def take_damage(self, dmg: int):
        # TODO: evasion chance
        self.health -= dmg
        if self.check_alive():
            ...
        else:
            ...

    def check_alive(self) -> bool:
        if self.health <= 0:
            return False
        else:
            return True