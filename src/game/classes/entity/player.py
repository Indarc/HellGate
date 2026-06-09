from typing import Optional

from game.classes.inventory import DontEnoughSlotsError
from game.classes.items import EquipItem
from config import loggers

from .entity import Entity
from game.classes.quests.default_quest import Quest
from game.classes.items import *


class Player(Entity):
    def __init__(self, name: Optional[str]=None, data: Optional[dict]=None):
        super().__init__(name=name, data=data)
        self.money = data.get("money") if data and data.get("money") else 0
        self.active_quest: Optional[Quest] = data.get("active_quest") if data and data.get("active_quest") else None

    def get_attributes(self) -> dict[str, int]:
        return self.attributes.to_dict()

    def banner(self) -> str:
        exp = self.level.get_experience()
        text = f"""
┌────── ▰▰☆▰▰ ──────┐
 ───❤️HP: {self.get_health()}/{self.get_max_health()}
 ───Имя: {self.name}
 ───Уровень: {self.get_level()}
 ───Опыт: {exp[0]}/{exp[1]}

 ───⚔️Урон: {self.get_damage().interface()}
 ───🛡️Броня: {self.get_armor_rating()}
 ───👟Уклонение: {self.get_evasion_rating()}
 ───🎯Точность: {self.get_accuracy_rating()}

 ───Атрибуты:
 ───💪Сила: {self.attributes.get_strength()}
 ───🤲Ловкость: {self.attributes.get_agility()}
 ───🧠Интелект: {self.attributes.get_intelligence()}
└────── ▰▰☆▰▰ ──────┘
"""
        return text

    def to_dict(self) -> dict:
        entity_dict = super().to_dict()
        update_info = {
            "_": "Player",
            "money": self.money,
            "active_quest": self.active_quest.to_dict() if self.active_quest is not None else None
        }
        entity_dict.update(update_info)
        return entity_dict
