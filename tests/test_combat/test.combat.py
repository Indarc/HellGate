import pytest

from game.classes.entity import Entity


class TestCombat:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.entity_one = Entity(name="Entity_One")
        self.entity_two = Entity(name="Entity_Two")