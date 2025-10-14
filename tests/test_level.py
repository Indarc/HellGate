import pytest

from server.classes.entity import Level, Stats


class TestLevel:
    def test_lvl_up(self):
        stats = Stats()
        lvl = Level(tracking_stats=stats)

        lvl.lvl_up()
        assert stats.stamina == 6
        assert stats.power == 6
        assert lvl.experience == 0
        assert lvl.max_experience == 20
    
    def test_add_exp(self):
        ...