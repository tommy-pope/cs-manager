from .data.player.player import *
from .engine.game_engine import GameEngine, Team
from .data.team.team_information import TeamInformation


def main():
    team_one = Team(TeamInformation("Team One"))
    team_two = Team(TeamInformation("Team One"))

    engine = GameEngine()
    engine.play_game(team_one, team_two)
