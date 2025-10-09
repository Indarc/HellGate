import pytest

from server.classes.player import Player
from server.classes.entity import Entity


class TestPlayer:
    def test_atack(self):
        player = Player("Player")
        enemy = Entity("Enemy")

        player.atack(enemy)
        assert enemy.health < enemy.max_health()
