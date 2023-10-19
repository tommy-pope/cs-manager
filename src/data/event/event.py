from ..match.match import Match

class Event:
    def __init__(self, id: int, name: str, rep: float, start_date: list, end_date: list, type: str, teams: list, continent: str = None, related_events: list = None) -> None:
        self.id = id
        self.name = name
        self.rep = rep
        self.start_date = start_date
        self.end_date = end_date
        self.type = type
        self.continent = continent
        self.related_events = related_events

        self.teams = teams
        self.active_teams = teams

        self.total_rounds = len(self.teams) 
        self.current_rounds = 0
        self.matches = []

    def eliminate_team(self, team) -> None:
        for t in self.active_teams:
            if t.info.id == team.info.id:
                self.active_teams.remove(t)
                break
    
    def generate_matches(self, db) -> None:
        num_matches = len(self.active_teams) // 2

        matches = [Match(self.active_teams[i], self.active_teams[-i - 1], self.start_date, self) for i in range(num_matches)]

        db.matches.extend(matches)
        self.matches.extend(matches)

        

