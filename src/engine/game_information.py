from ..data.player.player import Player


class GameInformation:
    def __init__(self) -> None:
        self.current_round = 0

        self.last_round_winner = 0

        self.is_overtime = False
        self.rounds_to_reach = 16

        self.team_one_score = 0
        self.team_two_score = 0

        self.team_one_alive = []
        self.team_two_alive = []

        self.team_one_surviving = 0
        self.team_two_surviving = 0

        self.team_one_lossbonus = 1
        self.team_two_lossbonus = 1

        self.team_one_money = 4000
        self.team_two_money = 4000

        self.team_one_buy = "save"
        self.team_two_buy = "save"
