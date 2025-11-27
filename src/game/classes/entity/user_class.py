from .player import Player

from server.loggers import Loggers


class User:
    def __init__(self, id, player: Player=None, status: bool=True, data: dict=None):
        if data:
            t = data.get("_")
            if t != "User":
                Loggers.game_classes.error(f"[USER_INIT] Not supported dict to initialize User object: {t}")
                return
            
            user_id = data.get("id")
            if user_id != id:
                Loggers.game_classes.error(f"[USER_INIT] User id from dict not equal telegram user id: {id} != {user_id}")
                return
            
            player_dict = data.get("player")
            if not player_dict:
                Loggers.game_classes.error("[USER_INIT] Player dict missing")
                return
            self.id: int = id
            self.player = Player(data=player_dict)

        else:
            if not id or not player:
                Loggers.game_classes.error("User class requered parameters to initialize")
                return
            self.id: int = id
            self.player: Player = player
    
    def to_dict(self) -> dict:
        return {
            "_": "User",
            "id": self.id,
            "player": self.player.to_dict()
        }