import pytest

from server.classes.entity import Entity


class TestEntity:
    def test_atack(self):
        Player = Entity("Player")
        Enemy = Entity("Enemy")

        Player.atack(Enemy)
        assert Enemy.health < Enemy.max_health()
    
    @pytest.mark.parametrize(
            "exp, total_lvl",
            [
                (1000, 14),
                (10, 2),
                (30, 3),
                (128, 5)
            ]
    )
    def test_lvl_up(self, exp, total_lvl):
        Player = Entity("Player")
        Player.level.add_exp(exp)
        assert Player.level.get_level() == total_lvl
    
    @pytest.mark.parametrize(
            "damage, alive",
            [
                (1, True),
                (5, True),
                (10, True),
                (1000000, False)
            ]
    )
    def test_alive(self, damage, alive):
        Player = Entity("Player")
        atack_result = Player.take_damage(damage)
        assert atack_result.alive == alive