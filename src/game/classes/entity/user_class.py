from typing import Optional, TYPE_CHECKING

from server.config import loggers

if TYPE_CHECKING:
    from .player import Player


class User:
    def __init__(self, id, player: Optional["Player"] = None, status: bool = True, data: Optional[dict] = None):
        if data:
            t = data.get("_")
            if t != "User":
                loggers.game_classes.error(f"[USER_INIT] Not supported dict to initialize User object: {t}")
                return
            
            user_id = data.get("id")
            if user_id != id:
                loggers.game_classes.error(f"[USER_INIT] User id from dict not equal telegram user id: {id} != {user_id}")
                return
            
            player_dict = data.get("player")
            if not player_dict:
                loggers.game_classes.error("[USER_INIT] Player dict missing")
                return
            self.id: int = id
            from .player import Player
            self.player = Player(data=player_dict)

        else:
            if not id or not player:
                loggers.game_classes.error("User class requered parameters to initialize")
                return
            self.id: int = id
            self.player: "Player" = player
    
    def to_dict(self) -> dict:
        return {
            "_": "User",
            "id": self.id,
            "player": self.player.to_dict()
        }