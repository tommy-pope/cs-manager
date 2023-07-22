from ..player.player import Player

class Team():
    def __init__(self, name: str) -> None:
        self.name = name
        self.players = []

    def add_player(self, player: Player):
        self.players.append(player)