from ..player.player import Player


class TeamInformation:
    def __init__(self, name: str) -> None:
        self.name = name
        self.players = []
