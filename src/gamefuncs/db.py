from ..data.continent.continent import Continent
from ..data.nation.nation import Nation

from ..data.player.player import Player

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

            print(f"{continent}: {percentages}")





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
        eu_teams = 0
        na_teams = 10
        sa_teams = 0
        asia_teams = 0

        for teams in range(na_teams):




            self.generate_team(self.continents["NA"])

    def generate_team(self, continent: Continent):
        

        players = []

        while len(players) < 5:
            # no previous players generated
            if len(players) == 0:
                nation_chance = random.uniform(0, 1) * 100
                cumulative_weight = 0
                nation = None

                for name in continent.nation_distribution:
                    cumulative_weight += continent.nation_distribution[name] / 100
                    if nation_chance <= cumulative_weight:
                        nation = continent.nations[name]
                        break

                player = self.generate_player(nation)
                players.append(player)

    def generate_player(self, nation: Nation) -> Player:
        pass