from .item_import import items


class Item: # base class for all items
    """Default item class"""
    def __init__(self, id:int, data: dict=None):
        if data:
            self.id: int = data.get("id")
            self.name: str = data.get("name")
            self.cost: float = data.get("cost")
            self.description: str = data.get("description")
            self.emoji: str = data.get("emoji")
            self.stacked: bool = data.get("stacked")
        else:
            self.item_dict: dict = items.get(id)
            self.id = self.item_dict.get("id")
            self.name: str = self.item_dict.get("name")
            self.cost: float = self.item_dict.get("cost")
            self.description: str = self.item_dict.get("description")
            self.emoji: str = self.item_dict.get("emoji")
            self.stacked: bool = self.item_dict.get("stacked")
            # TODO: item image
    
    def banner(self) -> str:
        text = f"""
{self.name}
--------------------
{self.description}
"""
        return text

    def to_dict(self) -> dict:
        return {
            "_": "item",
            "id": self.id,
            "name": self.name,
            "cost": self.cost,
            "description": self.description,
            "emoji": self.emoji,
            "stacked": self.stacked
        }