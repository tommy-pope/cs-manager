from ..match.match import Match

from ...engine.game_engine import GameEngine

from ...gamefuncs.utility import find_closest_square, add_to_date, check_date_equality, subtract_from_date

from math import ceil, log2

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
        self.active_teams = teams.copy()

        self.placements = {i: None for i in range(1, len(self.active_teams))}

        self.round = 0
        self.total_rounds = 0

        self.matches = []
        self.results = []

    def eliminate_team(self, team) -> None:
        for t in self.active_teams:
            if t.info.id == team.info.id:
                self.placements[len(self.active_teams)] = team
                self.active_teams.remove(t)
                break
    
    def generate_matches(self, db) -> None:
        if len(self.matches) > 0:
            return

        if self.type == "qual":
            self.generate_bracket_matches(db)
        elif self.type == "main" and self.round == 0:
            self.generate_group_matches(db)
        elif self.type == "main" and self.round != 0:
            self.generate_bracket_matches(db)

        db.games_generated = True

    def generate_bracket_matches(self, db) -> None:
        # winner
        if len(self.active_teams) == 1:
            self.placements[1] = self.active_teams[0]

            db.past_events.append(self)
    
            for e in db.events:
                # send winner of qual to main event
                if self.related_events is not None and e.id == self.related_events[0].id and self.type == "qual":
                    e.teams.append(self.placements[1])
                    e.active_teams.append(self.placements[1])
                    e.placements = {i: None for i in range(1, len(e.active_teams))}

                if e.id == self.id:
                    db.events.remove(e)

        closest_square = find_closest_square(len(self.active_teams))

        # set total rounds if first round
        if self.round == 0:
            if len(self.teams) == closest_square:
                self.total_rounds = int(log2(closest_square))
            else:
                tmp = closest_square

                while tmp > 1:
                    tmp = tmp / 2
                    self.total_rounds += 1
                
                self.total_rounds += 1
                
        self.round += 1

        if closest_square != len(self.active_teams):
            num_matches = len(self.active_teams) - closest_square
            teams_in_round = num_matches * 2

            start_idx = len(self.active_teams) - teams_in_round
            end_idx = start_idx + teams_in_round
            avail_teams = self.active_teams[start_idx:end_idx]

            matches = [Match(avail_teams[i], avail_teams[-i -1], self.start_date, self, self.round) for i in range(num_matches)]
            db.matches.extend(matches)
            self.matches.extend(matches)
        else:
            num_matches = round(len(self.active_teams) / 2)
            
            if self.type == "qual":
                game_date = add_to_date(self.start_date, days=1) if self.round > ceil(self.total_rounds / 2) else self.start_date
            else:
                game_date = add_to_date(self.start_date, days=self.round + 1)

            matches = [Match(self.active_teams[i], self.active_teams[-i - 1], game_date, self, self.round) for i in range(num_matches)]
            db.matches.extend(matches)
            self.matches.extend(matches)
    
    def generate_group_matches(self, db) -> None:
        self.total_rounds = int(log2(int(len(self.teams) / 2)) + 1)
        self.round = 1

        total_groups = int(len(self.teams) / 4)

        self.groups = [[] for i in range(total_groups)]
        
        for i in range(len(self.teams)):
            self.teams[i].wins = 0
            self.teams[i].losses = 0
            self.teams[i].round_difference = 0
            self.groups[i % 4].append(self.teams[i])

        for i, group in enumerate(self.groups):
            m1 = Match(group[0], group[3], self.start_date, self, 1)
            m2 = Match(group[1], group[2], self.start_date, self, 1)

            m3 = Match(group[2], group[0], add_to_date(self.start_date, days=1), self, 1)
            m4 = Match(group[3], group[1], add_to_date(self.start_date, days=1), self, 1)

            m5 = Match(group[0], group[1], add_to_date(self.start_date, days=2), self, 1)
            m6 = Match(group[2], group[3], add_to_date(self.start_date, days=2), self, 1)

            self.matches.extend([m1, m2, m3, m4, m5, m6])
            db.matches.extend([m1, m2, m3, m4, m5, m6])

        db.games_generated = True

    def play_match(self, db, match) -> None:
        engine = GameEngine(debug=False)

        finished_game = engine.play_game(match.team_one, match.team_two)

        team_one_score = finished_game.game_information.team_one_score
        team_two_score = finished_game.game_information.team_two_score

        match.scores.extend([team_one_score, team_two_score])
        match.game_stats = finished_game.game_stats

        if team_one_score > team_two_score:
            match.winner = match.team_one
            match.loser = match.team_two

            # group stage
            if self.type == "main" and self.round == 1:
                match.team_one.wins += 1
                match.team_one.round_difference += team_one_score - team_two_score
                match.team_two.round_difference += team_two_score - team_one_score
                match.team_two.losses += 1
            else:
                match.event.eliminate_team(match.team_two)

        else:
            match.winner = match.team_two
            match.loser = match.team_one

            # group stage
            if self.type == "main" and self.round == 1:
                match.team_two.wins += 1
                match.team_one.round_difference += team_one_score - team_two_score
                match.team_two.round_difference += team_two_score - team_one_score
                match.team_one.losses += 1
            else:
                match.event.eliminate_team(match.team_one)

        self.results.append(match)
        self.matches.remove(match)

        db.results.append(match)
        db.matches.remove(match)


        

