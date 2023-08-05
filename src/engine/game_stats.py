from ..data.team.team import Team


class GameStats:
    def __init__(self) -> None:
        self.team_one_stats = {}
        self.team_two_stats = {}

    def load_blank_stats(self, team_one: Team, team_two: Team) -> None:
        blank_stats = {
            "kills": 0,
            "assists": 0,
            "deaths": 0,
            "first_bloods": 0,
            "clutches": 0,
            "multikills": 0,
            "damage": 0,
            "fpr": 0,
            "fbpr": 0,
            "cpr": 0,
            "adr": 0,
            "rating": 0,
        }

        for player in team_one.info.players:
            self.team_one_stats[player.info.player_id] = blank_stats.copy()

        for player in team_two.info.players:
            self.team_two_stats[player.info.player_id] = blank_stats.copy()
