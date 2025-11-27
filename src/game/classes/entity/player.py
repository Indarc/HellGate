from .entity import Entity
from game.classes.inventory import Inventory
from game.classes.quests.default_quest import Quest

class Player(Entity):
    def __init__(self, name: str=None, data: dict=None):
        if data:
            super().__init__(name, data=data)
            self.money = data.get("money")
            self.inventory = Inventory(data=data.get("inventory"))
            self.quests = [Quest(data=x) for x in data.get("quests")]
            self.active_quest: Quest | None = self.quests[data.get("active_quest")] if data.get("active_quest") is not None else None
        else:
            if not name:
                return
            super().__init__(name)
            self.money = 0
            self.inventory = Inventory()
            self.quests = [Quest(index=x) for x in Quest.all_quests.keys()]
            self.active_quest: Quest | None = None

    def banner(self) -> str: # TODO: to player banner
        exp = self.level.get_experience()
        text = f"""
┌────── ▰▰☆▰▰ ──────┐
 ───❤️HP: {self.health}/{self.max_health()}
 ───Имя: {self.name}
 ───Уровень: {self.level.get_level()}
 ───Опыт: {exp[0]}/{exp[1]}

 ───⚔️Урон: {self.damage()}
 ───🛡️Броня: {self.armor}
 ───👟Уклонение: {self.evasion()}%
 ───🎯Точность: {self.stats.accuracy}%

 ───Атрибуты:
 ───🫀Выносливость: {self.stats.stamina}
 ───💪Сила: {self.stats.power}
 ───🤲Ловкость: {self.stats.agility}
 ───🧠Интелект: {self.stats.intelligence}
└────── ▰▰☆▰▰ ──────┘
"""
        return text

    def to_dict(self) -> dict:
        dict_return = {
            "_": "Player",
            "money": self.money,
            "name": self.name,
            "stats": self.stats.to_dict(),
            "level": self.level.to_dict(), # TODO
            "health": self.health,
            "armor": self.armor,
            "inventory": self.inventory.to_dict(),
            "quests": [x.to_dict() for x in self.quests],
            "active_quest": self.active_quest.to_dict() if self.active_quest is not None else None
        }
        return dict_return
