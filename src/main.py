from .data.player.player import *
from .data.team.team import Team


def main():
    team_one = Team("Team One")
    team_two = Team("Team Two")

    for i in range(5):
        info = PlayerInformation(f"Player{i}")
        attributes = PlayerAttributes()
