from .player_attributes import PlayerAttributes
from .player_information import PlayerInformation

from .player_stats_constants import progression_odds, attribute_changes

import random


class Player:
    def __init__(
        self, player_information: PlayerInformation, player_attributes: PlayerAttributes
    ) -> None:
        self.info = player_information
        self.attributes = player_attributes

    def monthly_progression_or_regression(self):
        odds = progression_odds[self.info.age]
        output = random.choices(attribute_changes, weights=odds, k=6)

        attribute_deltas = []

        for number in output:
            if number == 1 or number == .3:
                if self.attributes.overall >= self.attributes.potential:
                    number = 0

            number2 = 0

            if number == 1:
                number2 = .3
            elif number == .3 or number == 0 or number == -.3:
                number2 = 0
            elif number == -1:
                number2 = -.3
                
            attribute_deltas.append(round(random.uniform(number, number2), 2))

        for idx in range(len(attribute_deltas)):
            if idx == 0:
                self.attributes.rifle = round(self.attributes.rifle + attribute_deltas[idx], 2)
                if self.attributes.rifle > 100: self.attributes.rifle = 100

            elif idx == 1:
                self.attributes.pistol = round(self.attributes.pistol + attribute_deltas[idx], 2)
                if self.attributes.pistol > 100: self.attributes.pistol = 100
            elif idx == 2:
                self.attributes.awp = round(self.attributes.awp + attribute_deltas[idx], 2)
                if self.attributes.awp > 100: self.attributes.awp = 100
            elif idx == 3:
                self.attributes.positioning = round(self.attributes.positioning + attribute_deltas[idx], 2)
                if self.attributes.positioning > 100: self.attributes.positioning = 100
            elif idx == 4:
                self.attributes.clutch = round(self.attributes.clutch + attribute_deltas[idx], 2)
                if self.attributes.clutch > 100: self.attributes.clutch = 100
            elif idx == 5:
                self.attributes.consistency = round(self.attributes.consistency + attribute_deltas[idx], 2)
                if self.attributes.consistency > 100: self.attributes.consistency = 100

        self.attributes.overall = round(((self.attributes.rifle + self.attributes.pistol + self.attributes.awp + self.attributes.positioning + self.attributes.clutch + self.attributes.consistency) / 6), 2)

    def decide_retirement(self):
        # nothing for now
        #age_factor = self.info.age / 36
        #age_percentage = 100

        if self.info.age < 30:
            return
        
        if self.info.age == 30: chance_to_retire = .001
        elif self.info.age == 31: chance_to_retire = .002
        elif self.info.age == 32: chance_to_retire = .005
        elif self.info.age == 33: chance_to_retire = .008
        elif self.info.age == 34: chance_to_retire = .015
        elif self.info.age == 35: chance_to_retire = .05
        else: chance_to_retire = .1

        result = random.random() * 100

        if result <= chance_to_retire:
            self.retire()
    
    def retire(self):
        print("WE RETIRED!!!")