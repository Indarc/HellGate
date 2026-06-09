from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import AttackResult
    from game.classes.entity import Entity


class CombatManager:
    """Class for managing combat interactions"""
    def __init__(self):
        ...
    
    def atack(self, attacker: "Entity", target: "Entity") -> "AttackResult":
        attack_result = attacker.attack(target=target)
        return attack_result

    def get_experience(self, target: "Entity", enemy: "Entity") -> None:
        target.add_experience(enemy.get_level())