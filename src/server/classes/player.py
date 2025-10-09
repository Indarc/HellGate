from .entity import Entity


class Player(Entity):
    def __init__(self, name):
        super().__init__(name)

    def banner(self) -> str: # TODO: to player banner
        exp = self.level.get_experience()
        text = f"""
❤️HP: {self.health}/{self.max_health()}
Имя: {self.name}
Уровень: {self.level.get_level()}
Exp: {exp[0]}/{exp[1]}

⚔️Урон: {self.damage()}
🛡️Броня: {self.armor}
👟Уклонение: {self.evasion()}
🎯Точность: {self.stats.accuracy}

Атрибуты:
🫀Выносливость: {self.stats.stamina}
💪Сила: {self.stats.power}
🤲Ловкость: {self.stats.agility}
🧠Интелект: {self.stats.intelligence}
"""
        return text
