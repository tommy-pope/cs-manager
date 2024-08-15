from ..data.continent.continent import Continent
from ..data.nation.nation import Nation

from ..data.player.player import Player, PlayerInformation, PlayerAttributes, PlayerContract
from ..data.team.team import Team, TeamInformation
from ..data.event.event import Event

from .utility import (
    add_to_date,
    subtract_from_date,
    check_date_equality,
    find_team_in_event,
)

import csv
import random
from pathlib import Path

import pickle


class GameDB:
    def __init__(self) -> None:
        self.continents = {}
        self.nations = []
        self.teams = []
        self.players = []
        self.free_agents = []
        self.events = []
        self.matches = []
        self.results = []
        self.past_events = []

        self.date = [1, 1, 2023]

        self.available_team_names = []
        self.games_generated = False

    def setup_game(self) -> None:
        self.generate_continents()
        self.generate_nations()
        self.generate_teams()
        self.generate_free_agents()
        self.update_teams()
        self.rank_teams()

    def save_game(self) -> None:
        f = open("test.sav", "wb")
        pickle.dump(self, f, 2)
        f.close()

    @classmethod
    def load_game(cls):
        f = open("test.sav", "rb")
        return pickle.load(f)

    def generate_continents(self) -> None:
        eu = Continent("Europe", "EU", 90)
        na = Continent("North America", "NA", 80)
        sa = Continent("South America", "SA", 80)
        asia = Continent("Asia", "ASIA", 70)

        self.continents["EU"] = eu
        self.continents["NA"] = na
        self.continents["SA"] = sa
        self.continents["ASIA"] = asia

    def generate_nations(self) -> None:
        fp = Path("src/data/nation/nations.csv")
        with open(fp, "r") as file:
            reader = csv.reader(file, delimiter=",")
            for line in reader:
                name = line[0]
                sname = line[1]
                rep = float(line[2])
                continent = line[3]

                nation = Nation(name, sname, rep, continent)
                self.continents[continent].nations[sname] = nation

        for continent in self.continents.values():
            continent.calculate_nation_distribution()

    def generate_teams(self) -> None:
        # load team names
        fp = Path("src/data/team/teams.csv")
        with open(fp, "r") as file:
            reader = csv.reader(file, delimiter=",")
            for line in reader:
                name = line[0]
                type = line[1]

                self.available_team_names.append([name, type])

        teams_per_cont = {
            "EU": 40,
            "NA": 22,
            "SA": 21,
            "ASIA": 8,
        }

        for continent in self.continents:
            num_teams = teams_per_cont[continent]

            cont_rep = self.continents[continent].rep - 10

            if continent == "EU":
                biased_rep = cont_rep / 10
            else:
                biased_rep = cont_rep / 6

            cont_team_reps = [
                random.gauss(cont_rep, biased_rep) for _ in range(num_teams)
            ]

            for rep in cont_team_reps:
                if rep > 90:
                    rep -= random.randint(1,5)

            cont_team_reps = [round(max(30, min(100, x)), 2) for x in cont_team_reps]

            for team in range(num_teams):
                # select teamname
                team_name = random.choice(self.available_team_names)
                self.available_team_names.remove(team_name)
                team_name = team_name[0]

                self.generate_team(
                    team_name, self.continents[continent], cont_team_reps[team]
                )

            self.continents[continent].calculate_team_rankings()

    def generate_team(self, team_name: str, continent: Continent, team_rep: float):
        players = []
        awp_generated = False

        while len(players) < 5:
            is_awper = False

            if not awp_generated:
                awp_chance = 0.2 + 0.2 * len(players)
                rand = random.random()

                is_awper = True if rand <= awp_chance else False
                awp_generated = is_awper

            # no previous players generated
            if len(players) == 0:
                nation_chance = random.uniform(0, 1) * 100
                cumulative_weight = 0
                nation = None

                for name in continent.nation_distribution:
                    cumulative_weight += continent.nation_distribution[name]
                    if nation_chance <= cumulative_weight:
                        nation = continent.nations[name]
                        break

                player = self.generate_player(team_rep, nation, is_awper)
                players.append(player)
                self.players.append(player)
            else:
                rand = random.random()
                player_nat = None

                # chance to get same nation as teammate
                if rand < 0.7:
                    player_nat = self.continents[continent.sname].nations[
                        random.choice(players).info.nationality
                    ]
                else:
                    nation_chance = random.uniform(0, 1) * 100
                    cumulative_weight = 0

                    for name in continent.nation_distribution:
                        cumulative_weight += continent.nation_distribution[name]
                        if nation_chance <= cumulative_weight:
                            player_nat = continent.nations[name]
                            break

                player = self.generate_player(team_rep, player_nat, is_awper)
                players.append(player)
                self.players.append(player)

        # generate team finance
        if team_rep >= 80:
            max_budget = 20000000
            min_budget = 5000000
        elif team_rep >= 70 and team_rep < 80:
            max_budget = 10000000
            min_budget = 2500000
        elif team_rep >= 60 and team_rep < 70:
            max_budget = 5000000
            min_budget = 1500000
        else:
            max_budget = 2500000
            min_budget = 500000

        budget = random.randint(min_budget, max_budget) 

        team_info = TeamInformation(
            len(self.teams), team_name, team_rep, players, continent, "average", budget
        )
        team = Team(team_info)

        for player in team.info.players:
            player.contract.team = team.info.id

        self.teams.append(team)
        continent.teams.append(team)

    def generate_player(self, teamrep: float, nation: Nation, is_awper: bool) -> Player:
        pid = 0 if len(self.players) == 0 else self.players[-1].info.player_id + 1
        age = round(max(16, min(35, random.gauss(23, 23 / 4))))

        player_info = PlayerInformation(pid, f"test_{pid}", age, nation.sname)

        rifle_mean = (
            pistol_mean
        ) = awp_mean = positioning_mean = clutch_mean = consistency_mean = teamrep
        awp_mean = awp_mean - 20 if not is_awper else awp_mean

        rifle = round(max(0, min(100, random.gauss(rifle_mean, rifle_mean / 8))), 2)
        pistol = round(max(0, min(100, random.gauss(pistol_mean, pistol_mean / 8))), 2)
        awp = round(max(0, min(100, random.gauss(awp_mean, awp_mean / 8))), 2)
        positioning = round(
            max(0, min(100, random.gauss(positioning_mean, positioning_mean / 8))), 2
        )
        clutch = round(max(0, min(100, random.gauss(clutch_mean, clutch_mean / 8))), 2)
        consistency = round(
            max(0, min(100, random.gauss(consistency_mean, consistency_mean / 8))), 2
        )
        overall = round(((rifle + pistol + awp + positioning + clutch + consistency) / 6), 2)

        if age > 30:
            potential = overall
        else:
            potential = round(
                max(overall, min(100, random.gauss(teamrep, teamrep / 8)))
            )

        player_attributes = PlayerAttributes(
            rifle,
            pistol,
            awp,
            positioning,
            clutch,
            consistency,
            overall,
            potential,
            is_awper,
        )

        # calcuate initial contract
        base_salary = 30000 * (1.05 ** (teamrep - 70))
        age_scaling_factor = 1.5 - abs(25 - age) / 25

        # younger and older players get worse contracts
        if age < 20:
            age_discount = random.uniform(5000, 10000) * age_scaling_factor
            base_salary -= age_discount
        elif age > 30:
            age_discount = random.uniform(2000, 5000) * age_scaling_factor
            base_salary -= age_discount

        random_factor = random.uniform(-5000, 5000)
        base_salary += random_factor
        base_salary = round(base_salary)

        player_contract = PlayerContract(None, base_salary, self.date, add_to_date(self.date, years=3))
        return Player(player_info, player_attributes, player_contract)

    def generate_events(self):
        # generate tier one event
        if self.date[0] % 2 != 0 and self.date[1] == 1:
            self.generate_event(
                "Tier One Event", 90, add_to_date(self.date, months=1), "main"
            )

        # generate tier two event
        #self.generate_event("Tier Two Event", 75)

        # generate tier three events
        if self.date[0] != 11 and self.date[1] == 15:
            for continent in self.continents:
                chance = random.random()

                # 33% chance to generate lowtier event for region
                if chance <= .33:
                    self.generate_event("Tier Three Event", 60, add_to_date(self.date, months=1), "main", continent)

    def generate_event(
        self,
        event_name: str,
        event_rep: float,
        start_date: list,
        type: str,
        continent: str = None,
        parent_event: Event = None,
    ) -> None:
        event_id = 0 if len(self.events) == 0 else self.events[-1].id + 1

        # if tier one event, create qualifier
        if event_rep > 85:
            invited_teams = self.teams[:12]
            for team in invited_teams:
                team.wins = 0
                team.losses = 0

            event = Event(
                event_id,
                event_name,
                event_rep,
                start_date,
                add_to_date(start_date, days=5),
                type,
                invited_teams,
                "WORLD",
                [],
            )

            # store event on team
            for team in event.teams:
                team.events.append(event)

            event.groups = None
            self.events.append(event)

            self.generate_event(
                f"{event_name} Qualifier EU",
                event_rep - 20,
                subtract_from_date(start_date, days=16),
                "qual",
                "EU",
                event,
            )
            self.generate_event(
                f"{event_name} Qualifier NA",
                event_rep - 20,
                subtract_from_date(start_date, days=16),
                "qual",
                "NA",
                event,
            )
            self.generate_event(
                f"{event_name} Qualifier SA",
                event_rep - 20,
                subtract_from_date(start_date, days=16),
                "qual",
                "SA",
                event,
            )
            self.generate_event(
                f"{event_name} Qualifier ASIA",
                event_rep - 20,
                subtract_from_date(start_date, days=16),
                "qual",
                "ASIA",
                event,
            )
        elif event_rep > 70:
            pass
        elif event_rep <= 70 and type == "qual":
            available_teams = []

            for team in self.continents[continent].teams:
                if not find_team_in_event(parent_event, team):
                    available_teams.append(team)

            event = Event(
                event_id,
                event_name,
                event_rep,
                start_date,
                add_to_date(start_date, days=1),
                "qual",
                available_teams,
                continent,
                [parent_event],
            )

            # store event on team
            for team in event.teams:
                team.events.append(event)

            event.generate_matches(self)
            self.events.append(event)
            parent_event.related_events.append(self)
        elif event_rep <= 70 and type == "main":
            # regional event
            if continent is not None:
                invited_teams = [team for team in self.continents[continent].teams if abs(team.info.reputation - event_rep) <= 20 or team.info.reputation < event_rep]

                event = Event(event_id, event_name, event_rep, start_date, add_to_date(start_date, days=1), type, invited_teams, continent, [])

                for team in event.teams:
                    team.events.append(event)
                
                event.generate_matches(self)
                self.events.append(event)

    def generate_free_agents(self):
        number_of_players_to_gen = random.randint(3, 10)
        cont_choice = random.choices(population=["EU", "NA", "SA", "ASIA"], weights=[.45, .25, .25, .05], k=number_of_players_to_gen)
        rep_choice = random.choices(population=[60, 70, 80, 85], weights=[.6, .33, .05, .02], k=number_of_players_to_gen)

        for i in range(number_of_players_to_gen):
            player_cont = cont_choice[i]
            player_nation = random.choices(population=list(self.continents[player_cont].nation_distribution.keys()), weights=list(self.continents[player_cont].nation_distribution.values()), k=1)[0]
            player_nation = self.continents[player_cont].nations[player_nation]

            player_rep = rep_choice[i]

            # 20% chance to be awper
            result = random.random()
            if result <= .2:
                is_awper = True
            else:
                is_awper = False

            pid = 0 if len(self.players) == 0 else self.players[-1].info.player_id + 1
            # 16 - 25
            age = round(max(16, min(25, random.gauss(23, 23 / 4))))
            player_info = PlayerInformation(pid, f"test_{pid}", age, player_nation.sname)

            rifle_mean = (
                pistol_mean
            ) = awp_mean = positioning_mean = clutch_mean = consistency_mean = player_rep
            awp_mean = awp_mean - 20 if not is_awper else awp_mean

            rifle = round(max(0, min(100, random.gauss(rifle_mean, rifle_mean / 8))), 2)
            pistol = round(max(0, min(100, random.gauss(pistol_mean, pistol_mean / 8))), 2)
            awp = round(max(0, min(100, random.gauss(awp_mean, awp_mean / 8))), 2)
            positioning = round(
                max(0, min(100, random.gauss(positioning_mean, positioning_mean / 8))), 2
            )
            clutch = round(max(0, min(100, random.gauss(clutch_mean, clutch_mean / 8))), 2)
            consistency = round(
                max(0, min(100, random.gauss(consistency_mean, consistency_mean / 8))), 2
            )
            overall = round(((rifle + pistol + awp + positioning + clutch + consistency) / 6), 2)

            potential = round(
                max(overall, min(100, random.gauss(player_rep, player_rep / 8)))
            )

            player_attributes = PlayerAttributes(
                rifle,
                pistol,
                awp,
                positioning,
                clutch,
                consistency,
                overall,
                potential,
                is_awper,
            )

            new_player = Player(player_info, player_attributes, None)

            self.players.append(new_player)
            self.free_agents.append(new_player)

    def advance(self, ui, days) -> None:
        day = 0

        while day < days:
            # end of year
            if self.date[0] == 12 and self.date[1] == 31:
                for player in self.players:
                    player.info.age += 1

            if self.date[1] == 31:
                self.generate_free_agents()
                self.update_players()
                self.update_teams()
                self.rank_teams()

            self.check_for_matches()  
            self.generate_event_rounds()

            while self.games_generated:
                self.check_for_matches()
                self.generate_event_rounds()

            self.generate_events()
            self.date = add_to_date(self.date, days=1)
            ui.update_date()

            day += 1

        # self.save_game()

    def update_players(self) -> None:
        for player in self.players:
            player.decide_retirement(self)
            player.monthly_progression_or_regression()

    def update_teams(self) -> None:
        for team in self.teams:
            team.update_budget()

            # need to sign players, maybe someone retired?
            if len(team.info.players) < 5:
                team.sign_player(self)

    def check_for_matches(self) -> None:
        i = 0

        while i < len(self.matches):
            match = self.matches[i]

            # match day is today
            if check_date_equality(self.date, match.date):
                match.event.play_match(self, match)

                # if group stage, sort groups
                if match.event.round == 1 and match.event.type == "main" and match.event.rep >= 80:
                    for m, group in enumerate(match.event.groups):
                        match.event.groups[m] = sorted(
                            group, key=lambda x: x.wins, reverse=True
                        )

                        # sort by round diff
                        three_win_teams = sorted(
                            list(filter(lambda x: x.wins == 3, match.event.groups[m])),
                            key=lambda x: x.round_difference,
                            reverse=True,
                        )
                        two_win_teams = sorted(
                            list(filter(lambda x: x.wins == 2, match.event.groups[m])),
                            key=lambda x: x.round_difference,
                            reverse=True,
                        )
                        one_win_teams = sorted(
                            list(filter(lambda x: x.wins == 1, match.event.groups[m])),
                            key=lambda x: x.round_difference,
                            reverse=True,
                        )
                        zero_win_teams = sorted(
                            list(filter(lambda x: x.wins == 0, match.event.groups[m])),
                            key=lambda x: x.round_difference,
                            reverse=True,
                        )

                        match.event.groups[m] = (
                            three_win_teams
                            + two_win_teams
                            + one_win_teams
                            + zero_win_teams
                        )

                i -= 1

            i += 1

        self.games_generated = False

    def generate_event_rounds(self) -> None:
        for event in self.events:
            if (
                len(event.results) > 0
                and event.type == "qual"
                and check_date_equality(self.date, event.results[-1].date)
            ):
                event.generate_matches(self)
            elif (
                event.type == "main"
                and check_date_equality(
                    self.date, subtract_from_date(event.start_date, days=7)
                )
                and len(event.matches) == 0
            ):
                event.generate_matches(self)
            elif (
                event.type == "main"
                and check_date_equality(
                    self.date, add_to_date(event.start_date, days=2)
                )
                and event.round == 1
                and event.rep >= 80
            ):
                for group in event.groups:
                    for i in range(len(group)):
                        if i > 1:
                            event.eliminate_team(group[i])

                event.generate_matches(self)
            elif event.type == "main" and check_date_equality(
                self.date, add_to_date(event.start_date, days=1 + event.round)
            ):
                event.generate_matches(self)
            elif event.type == "main" and event.rep <= 60 and len(event.results) > 0 and check_date_equality(self.date, event.results[-1].date):
                event.generate_matches(self)

    def rank_teams(self) -> None:
        self.teams.sort(key=lambda x: x.info.elo, reverse=True)

        for i in range(len(self.teams)):
            self.teams[i].info.world_rank = i + 1

        for continent in self.continents.values():
            continent.calculate_team_rankings()
