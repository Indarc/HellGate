from typing import Optional

from .item import Item


class Material(Item):
    def __init__(self, data: Optional[dict]=None):
        super().__init__(data)