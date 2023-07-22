from ..data.player.player import Player

class GameInformation():
    def __init__(self) -> None:
        self.current_round = 0
        
        self.team_one_alive = []
        self.team_two_alive = []
        
        self.team_one_lossbonus = 1
        self.team_two_lossbonus = 1

        self.team_one_buy = "save"
        self.team_two_buy = "save"

