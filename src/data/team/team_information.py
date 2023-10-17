from ..player.player import Player


class TeamInformation:
    def __init__(self, name: str, reputation: float) -> None:
        self.name = name
        self.reputation = reputation
        self.players = []
