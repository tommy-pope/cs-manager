class Match:
    def __init__(self, team_one, team_two, date: list, event) -> None:
        self.team_one = team_one
        self.team_two = team_two
        self.date = date
        self.event = event

        self.scores = []

        self.winner = None
        self.loser = None

        self.game_stats = None