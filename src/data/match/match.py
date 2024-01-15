class Match:
    def __init__(self, team_one, team_two, date: list, event, round_in_event, bo) -> None:
        self.team_one = team_one
        self.team_two = team_two
        self.date = date
        self.event = event
        self.round_in_event = round_in_event
        self.bo = bo

        self.scores = []

        self.winner = None
        self.loser = None

        self.game_stats = []

    # https://www.geeksforgeeks.org/elo-rating-algorithm/
    def assign_elo(self):
        p2 = 1.0 * 1.0 / (1 + 1.0 * pow(10, 1.0 * (self.team_one.info.elo - self.team_two.info.elo) / 400))
        p1 = 1.0 * 1.0 / (1 + 1.0 * pow(10, 1.0 * (self.team_two.info.elo - self.team_one.info.elo) / 400))

        if self.winner == self.team_one:
            self.team_one.info.elo = round(self.team_one.info.elo + 15 * (1 - p1), 2)
            self.team_two.info.elo = round(self.team_two.info.elo + 15 * (0 - p2), 2)
        elif self.winner == self.team_two:
            self.team_one.info.elo = round(self.team_one.info.elo + 15 * (0 - p1), 2)
            self.team_two.info.elo = round(self.team_two.info.elo + 15 * (1 - p2), 2)