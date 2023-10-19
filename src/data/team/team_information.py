from ..player.player import Player


class TeamInformation:
    def __init__(self, id: int, name: str, reputation: float, players: list) -> None:
        self.id = id
        self.name = name
        self.reputation = reputation
        self.players = players
        self.elo = round(self.reputation * 10)
