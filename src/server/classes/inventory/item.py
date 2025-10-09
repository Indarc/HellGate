class Item:
    def __init__(self, id: int, name: str, cost: int, weight: float, description: str, emoji: str=None):
        self._id = id
        self.name = name
        self.cost = cost
        self.description = description
        self.emoji = emoji
        # TODO: item image
    
    def banner(self) -> str:
        text = f"""
{self.name}
--------------------
{self.description}
"""
        return text