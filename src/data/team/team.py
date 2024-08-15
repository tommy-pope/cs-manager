from .team_information import TeamInformation
from ..player.player_contract import PlayerContract

from ...gamefuncs.utility import add_to_date

import random


class Team:
    def __init__(self, team_information: TeamInformation) -> None:
        self.info = team_information
        
        self.events = []
        self.past_events = []

    def scout_player(self, player):
        actual_overall = player.attributes.overall
        actual_potential = player.attributes.potential

        scouted_overall = max(0, min(100, random.gauss(actual_overall, (1 - self.info.player_overall_scouting) * 30/1.5)))
        scouted_potential = max(0, min(100, random.gauss(actual_potential, (1 - self.info.player_potential_scouting) * 30/1.5)))

        return (scouted_overall, scouted_potential)

    def calculate_player_contract(self, player):
        # calcuate initial contract
        base_salary = 30000 * (1.05 ** (self.info.reputation - 70))
        age_scaling_factor = 1.5 - abs(25 - player.info.age) / 25

        # younger and older players get worse contracts
        if player.info.age < 20:
            age_discount = random.uniform(5000, 10000) * age_scaling_factor
            base_salary -= age_discount
        elif player.info.age > 30:
            age_discount = random.uniform(2000, 5000) * age_scaling_factor
            base_salary -= age_discount

        random_factor = random.uniform(-5000, 5000)
        base_salary += random_factor
        base_salary = round(base_salary)

        return base_salary

    def sign_player(self, db):
        # in future, maybe look at buying another player instead of just looking at free agents
        scouted_players = {}

        # check if need to replace awper
        replace_awp = True

        for player in self.info.players:
            if player.attributes.is_awper:
                replace_awp = False
                break

        # for now, only look at free agents in same cont, for future, if rep is high enough/can afford, import players
        for idx, player in enumerate(db.free_agents):
            if player.info.nationality in self.info.continent.nations.keys():
                if player.attributes.is_awper == replace_awp:
                    scouted_players[idx] = self.scout_player(player) 

        player_to_sign = None
        player_to_sign_scouting = None

        for index in scouted_players:
            player = db.free_agents[index]
            wanted_salary = self.calculate_player_contract(player)

            if (self.info.leftover_salary_budget - wanted_salary) >= 0:
                if player_to_sign is None:
                    player_to_sign = player
                    player_to_sign_scouting = scouted_players[index][0] + scouted_players[index][1] * 1.2
                    continue

                if scouted_players[index][0] + scouted_players[index][1] * 1.2  > player_to_sign_scouting:
                    player_to_sign = player
                    player_to_sign_scouting = scouted_players[index][0] + scouted_players[index][1] * 1.2
                    continue

        if player_to_sign is None:
            print("bruh no player found to sign")
            print(f"scout players: {len(scouted_players)}")
            print(f"leftover budget: {self.info.leftover_salary_budget}")
        
        contract = PlayerContract(self.info.id, wanted_salary, db.date, add_to_date(db.date, years=3))
        player_to_sign.contract = contract

        self.info.players.append(player_to_sign)

        print(f"{self.info.name} signed {player_to_sign.info.nickname} with salary of {player_to_sign.contract.salary}")

        self.update_budget()

    def update_finance_weights(self):
        test_salary_budget = round((self.info.budget * self.info.salary_split) / 12)

        for player in self.info.players:
            test_salary_budget -= player.contract.salary

        if test_salary_budget < 0:
            if self.info.salary_split < 1:
                self.info.salary_split += .1
                self.info.transfer_split -= .1

                self.update_finance_weights()

    def update_budget(self):
        self.update_finance_weights()

        self.info.transfer_budget = round(self.info.budget * self.info.transfer_split)
        self.info.salary_budget = round((self.info.budget * self.info.salary_split) / 12)
        self.info.leftover_salary_budget = self.info.salary_budget

        if self.info.more_transfer_budget:
            self.info.leftover_transfer_budget = self.info.transfer_budget
            self.info.more_transfer_budget = False

        # calculate leftover salary budget
        for player in self.info.players:
            self.info.leftover_salary_budget -= player.contract.salary