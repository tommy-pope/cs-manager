from .data.player.player import *
from .engine.game_engine import GameEngine, Team
from .data.team.team_information import TeamInformation


def main():
    team_one = Team(TeamInformation("Team One"))
    team_two = Team(TeamInformation("Team One"))

    for i in range(10):
        if i < 5:
            player = Player(PlayerInformation(i+1, f"Player{i+1}"), PlayerAttributes())
            team_one.info.players.append(player)
        else:
            player = Player(PlayerInformation(i+1, f"Player{i+1}"), PlayerAttributes())
            team_two.info.players.append(player)

    engine = GameEngine(debug=True)
    engine.play_game(team_one, team_two)