from ..data.continent.continent import Continent
from ..data.nation.nation import Nation

import csv
import os
from pathlib import Path

class GameDB:
    def __init__(self) -> None:
        self.continents = {}
        self.nations = []
        self.teams = []
        self.players = []
        self.events = []
    
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
                self.nations.append(nation)
                self.continents[continent].nations.append(nation)

    def generate_teams(self) -> None:
        eu_teams = 0
        na_teams = 10
        sa_teams = 0
        asia_teams = 0

        for teams in range(na_teams):

    def generate_team(self, nation: Nation):
