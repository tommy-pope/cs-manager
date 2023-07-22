from .game_information import GameInformation
from .game_stats import GameStats

from ..data.team.team import Team

class Game():
    def __init__(self, team_one: Team, team_two: Team, game_information: GameInformation, game_stats: GameStats) -> None:
        self.team_one = team_one
        self.team_two = team_two
        
        self.game_information = game_information
        self.game_stats = game_stats