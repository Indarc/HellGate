from typing import TYPE_CHECKING

from game.classes.items.damages import Damage

if TYPE_CHECKING:
    from game.classes.entity import Entity


class CombatManager:
    """Class for managing combat interactions"""
    def __init__(self):
        ...
    
    def atack(self, atacker: "Entity", target: "Entity") -> "AtackResult":
        alive = target.take_damage(atacker.get_damage())
        atack_result = AtackResult(alive, atacker.get_damage())
        return atack_result

    def get_experience(self, target: "Entity", enemy: "Entity") -> None:
        target.add_experience(enemy.get_level())


class AtackResult:
    def __init__(self, alive: bool, damaged: Damage):
        self.alive = alive
        self.damaged = damaged
