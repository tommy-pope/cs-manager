from ..data.continent.continent import Continent
from ..data.nation.nation import Nation

from ..data.player.player import Player, PlayerInformation, PlayerAttributes
from ..data.team.team import Team, TeamInformation
from ..data.event.event import Event

from .utility import add_to_date, subtract_from_date, find_team_in_event

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
        self.events = []
        self.matches = []

        self.date = [1, 1, 2023]
    
    def setup_game(self) -> None:
        self.generate_continents()
        self.generate_nations()
        self.generate_teams()
        self.rank_teams()

        self.generate_events()
    
    def save_game(self) -> None:
        f = open("test.sav", "wb")
        pickle.dump(self, f, 2)
        f.close()

    @classmethod
    def load_game(cls):
        f = open("test.sav", "rb")
        return pickle.load(f)

    def generate_continents(self) -> None:
        eu = Continent("Europe", "EU", 95)
        na = Continent("North America", "NA", 80)
        sa = Continent("South America", "SA", 85)
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
        teams_per_cont = {
            "EU": 20,
            "NA": 10,
            "SA": 10,
            "ASIA": 5,
        }

        for continent in self.continents:
            print(self.continents[continent].nation_distribution)
            num_teams = teams_per_cont[continent]

            cont_rep = self.continents[continent].rep - 10
            biased_rep = cont_rep / 8
        
            cont_team_reps = [random.gauss(cont_rep, biased_rep) for _ in range(num_teams)]
            cont_team_reps = [round(max(30, min(100, x)), 2) for x in cont_team_reps]

            print(f"{continent}: {cont_team_reps}")

            for team in range(num_teams):
                self.generate_team(self.continents[continent], cont_team_reps[team])
            
            self.continents[continent].calculate_team_rankings()

    def generate_team(self, continent: Continent, team_rep: float):
        team_name = "test"
        
        players = []
        awp_generated = False

        while len(players) < 5:
            is_awper = False

            if not awp_generated:
                awp_chance = .2 + .2 * len(players)
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

                #print(nation.sname)
                player = self.generate_player(team_rep, nation, is_awper)
                players.append(player)
                self.players.append(player)
            else:
                rand = random.random()
                player_nat = None

                # chance to get same nation as teammate
                if rand < .7:
                    player_nat = self.continents[continent.sname].nations[random.choice(players).info.nationality]
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

        team_info = TeamInformation(len(self.teams), team_name, team_rep, players)
        team = Team(team_info)

        self.teams.append(team)
        continent.teams.append(team)

    def generate_player(self, teamrep: float, nation: Nation, is_awper: bool) -> Player:
        pid = 0 if len(self.players) == 0 else self.players[-1].info.player_id + 1

        player_info = PlayerInformation(pid, f"test_{pid}", nation.sname)

        rifle_mean = pistol_mean = awp_mean = positioning_mean = clutch_mean = consistency_mean = teamrep
        awp_mean = awp_mean - 15 if not is_awper else awp_mean

        rifle = round(max(0, min(100, random.gauss(rifle_mean, rifle_mean/8))), 2)
        pistol = round(max(0, min(100, random.gauss(pistol_mean, pistol_mean/8))), 2)
        awp = round(max(0, min(100, random.gauss(awp_mean, awp_mean/8))), 2)
        positioning = round(max(0, min(100, random.gauss(positioning_mean, positioning_mean/8))), 2)
        clutch = round(max(0, min(100, random.gauss(clutch_mean, clutch_mean/8))), 2)
        consistency = round(max(0, min(100, random.gauss(consistency_mean, consistency_mean/8))), 2)

        player_attributes = PlayerAttributes(rifle, pistol, awp, positioning, clutch, consistency, is_awper)

        return Player(player_info, player_attributes)
    
    def generate_events(self):
        # generate tier one event
        self.generate_event("Tier One Event", 90, [2, 1, 2023], "main")

        # generate tier two event
        #self.generate_event("Tier Two Event", 75)

        # generate tier three events
        #self.generate_event("Tier Three Event", 60)

    def generate_event(self, event_name: str, event_rep: float, start_date: list, type: str, continent: str = None, parent_event: Event = None) -> None:
        event_id = 0 if len(self.events) == 0 else self.events[-1].id + 1

        # if tier one event, create qualifier
        if event_rep > 85:
            invited_teams = self.teams[:12]
            event = Event(event_id, event_name, event_rep, start_date, add_to_date(start_date, days=5), type, invited_teams)
            self.events.append(event)

            self.generate_event(f"{event_name} Qualifier EU", event_rep - 20, subtract_from_date(start_date, days=16), "qual", "EU", event)
            self.generate_event(f"{event_name} Qualifier NA", event_rep - 20, subtract_from_date(start_date, days=16), "qual", "NA", event)
            self.generate_event(f"{event_name} Qualifier SA", event_rep - 20, subtract_from_date(start_date, days=16), "qual", "SA", event)
            self.generate_event(f"{event_name} Qualifier ASIA", event_rep - 20, subtract_from_date(start_date, days=16), "qual", "ASIA", event)
        elif event_rep > 70:
            pass
        elif event_rep <= 70 and type == "qual":
            available_teams = []

            for team in self.continents[continent].teams:
                if not find_team_in_event(parent_event, team):
                    available_teams.append(team)

            event = Event(event_id, event_name, event_rep, start_date, add_to_date(start_date, days=1), "qual", available_teams, continent, [parent_event])
            self.events.append(event)

    def rank_teams(self):
        self.teams.sort(key=lambda x: x.info.elo, reverse=True)