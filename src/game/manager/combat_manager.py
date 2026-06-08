from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.classes.entity import Entity


class CombatManager:
    """Class for managing combat interactions"""
    def __init__(self):
        ...
    
    def atack(self, attacker: "Entity", target: "Entity") -> "AttackResult":
        alive, damage = attacker.attack(target=target)
        return AttackResult(alive, damage)

    def get_experience(self, target: "Entity", enemy: "Entity") -> None:
        target.add_experience(enemy.get_level())


class AttackResult:
    def __init__(self, alive: bool, damage: int):
        self.alive = alive
        self.damage = damage
