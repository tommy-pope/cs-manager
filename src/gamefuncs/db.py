from ..data.continent.continent import Continent
from ..data.nation.nation import Nation

from ..data.player.player import Player, PlayerInformation, PlayerAttributes

import csv
import random
from pathlib import Path

class GameDB:
    def __init__(self) -> None:
        self.continents = {}
        self.nations = []
        self.teams = []
        self.players = []
        self.events = []

        self.continents_distribution = {}
    
    def setup_game(self) -> None:
        self.generate_continents()
        self.generate_nations()
        self.generate_teams()

    def generate_continents(self) -> None:
        eu = Continent("Europe", "EU", 95)
        na = Continent("North America", "NA", 80)
        sa = Continent("South America", "SA", 85)
        asia = Continent("Asia", "AS", 70)

        self.continents["EU"] = eu
        self.continents["NA"] = na
        self.continents["SA"] = sa
        self.continents["ASIA"] = asia

        self.calculate_continent_distribution()

    def calculate_continent_distribution(self) -> None:
        for continent in self.continents:
            cont_obj = self.continents[continent]
            reputation = cont_obj.rep
            percentages = []

            for i in range(5):
                percentage = ((reputation/100) ** 3) / (i + 1)
                percentages.append(percentage)

            #print(f"{continent}: {percentages}")

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
            num_teams = teams_per_cont[continent]

            cont_rep = self.continents[continent].rep - 10
            biased_rep = cont_rep / 8
        
            cont_team_reps = [random.gauss(cont_rep, biased_rep) for _ in range(num_teams)]
            cont_team_reps = [round(max(30, min(100, x)), 2) for x in cont_team_reps]

            print(f"{continent}: {cont_team_reps}")

            for team in range(num_teams):
                self.generate_team(self.continents[continent], cont_team_reps[team])

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

                #print(nation_chance)
                #print(continent.nation_distribution)

                for name in continent.nation_distribution:
                    cumulative_weight += continent.nation_distribution[name]
                    if nation_chance <= cumulative_weight:
                        nation = continent.nations[name]
                        break

                player = self.generate_player(team_rep, nation, is_awper)
                players.append(player)
                self.players.append(player)
            else:
                # chance to get same nation as teammate
                pass


    def generate_player(self, teamrep: float, nation: Nation, is_awper: bool) -> Player:
        pid = 0 if len(self.players) == 0 else self.players[-1].info.player_id + 1

        player_info = PlayerInformation(pid, f"test_{pid}")

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
            