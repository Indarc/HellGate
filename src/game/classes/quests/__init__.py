import os
from pathlib import Path
import json

from paths import RESOURCES_DIR


def get_clear_quests() -> dict[int, dict]:
    quests_path = [Path(RESOURCES_DIR / "quests" / x) for x in os.listdir(RESOURCES_DIR / "quests") if x.endswith(".json")]
    quests = {}
    for i, path in enumerate(quests_path):
        with open(path, encoding="utf-8") as file:
            quest = json.load(file)
            quests.setdefault(i, quest)
    return quests


from .default_quest import Quest
from .errors import QuestAlreadyComplite
from .guide_line import GuideLine


__all__ = ["Quest", "QuestAlreadyComplite", "GuideLine"]