import copy
import random

from .game import Game, Team, GameInformation, GameStats
from ..data.player.player import Player


class GameEngine:
    def __init__(self, debug: str) -> None:
        self.game = None
        self.debug = debug

    # main entry point into the game simulation
    def play_game(self, team_one: Team, team_two: Team) -> Game:
        self.setup_game(team_one, team_two)
        self.simulate_game()

        return self.game

    def setup_game(self, team_one: Team, team_two: Team) -> None:
        game_stats = GameStats().load_blank_stats(team_one, team_two)

        self.game = Game(team_one, team_two, GameInformation(), game_stats)

    def simulate_game(self) -> None:
        # while the score of both teams is less than 16, and it is not 15-15
        while (
            self.game.game_information.team_one_score < 16
            and self.game.game_information.team_two_score < 16
            and not self.game.game_information.is_overtime
        ):
            if self.debug:
                input()

            self.setup_round()
            self.simulate_round()

    def repopulate_alive_lists(self) -> None:
        self.game.game_information.team_one_alive = copy.deepcopy(
            self.game.team_one.info.players
        )
        self.game.game_information.team_two_alive = copy.deepcopy(
            self.game.team_two.info.players
        )

        for player in self.game.game_information.team_one_alive:
            player.hp = 100
            player.hit_by = []

        for player in self.game.game_information.team_two_alive:
            player.hp = 100
            player.hit_by = []

    def update_economy(self) -> None:
        # if not first round, or halftime
        if (
            self.game.game_information.current_round != 1
            or self.game.game_information.current_round != 16
        ):
            team_one_money_to_add = 0
            team_two_money_to_add = 0

            if self.game.game_information.last_round_winner == 1:
                # if loss bonus is already 1, leave it. otherwise subtract by one
                self.game.game_information.team_one_lossbonus = (
                    1
                    if self.game.game_information.team_one_lossbonus == 1
                    else self.game.game_information.team_one_lossbonus - 1
                )
                # if loss bonus is already 5, leave it. otherwise add by one
                self.game.game_information.team_two_lossbonus = (
                    5
                    if self.game.game_information.team_two_lossbonus == 5
                    else self.game.game_information.team_two_lossbonus + 1
                )

                team_one_money_to_add = 5 * 3250
                team_two_money_to_add = 5 * (
                    1400 + 500 * (self.game.game_information.team_two_lossbonus - 1)
                )

            elif self.game.game_information.last_round_winner == 2:
                # if loss bonus is already 1, leave it. otherwise subtract by one
                self.game.game_information.team_two_lossbonus = (
                    1
                    if self.game.game_information.team_two_lossbonus == 1
                    else self.game.game_information.team_two_lossbonus - 1
                )
                # if loss bonus is already 5, leave it. otherwise add by one
                self.game.game_information.team_one_lossbonus = (
                    5
                    if self.game.game_information.team_one_lossbonus == 5
                    else self.game.game_information.team_one_lossbonus + 1
                )

                team_two_money_to_add = 5 * 3250
                team_one_money_to_add = 5 * (
                    1400 + 500 * (self.game.game_information.team_one_lossbonus - 1)
                )

            self.game.game_information.team_one_money += team_one_money_to_add
            self.game.game_information.team_two_money += team_two_money_to_add

            if self.game.game_information.team_one_money > 80000:
                self.game.game_information.team_one_money = 80000
            if self.game.game_information.team_two_money > 80000:
                self.game.game_information.team_two_money = 80000
        else:
            self.game.game_information.team_one_money = 4000
            self.game.game_information.team_two_money = 4000

    def team_one_purchase(self) -> None:
        if self.game.game_information.team_one_surviving != 0:
            last_round_buy = self.game.game_information.team_one_buy

            if last_round_buy == "save":
                self.game.game_information.team_one_money -= 12500 - (
                    800 * self.game.game_information.team_one_surviving
                )
                self.game.game_information.team_one_buy = "force"
            else:
                money_per_survivor = 0

                if last_round_buy == "force":
                    money_per_survivor = 3750
                elif last_round_buy == "full":
                    money_per_survivor = 5000
                elif last_round_buy == "full-awp":
                    money_per_survivor = 6000

                cost_to_full_awp = 30000 - (
                    money_per_survivor * self.game.game_information.team_one_surviving
                )

                cost_to_full = 25000 - (
                    money_per_survivor * self.game.game_information.team_one_surviving
                )

                cost_to_force = 12500 - (
                    money_per_survivor * self.game.game_information.team_one_surviving
                )

                if self.game.game_information.team_one_money >= (cost_to_full_awp):
                    self.game.game_information.team_one_money -= cost_to_full_awp
                    self.game.game_information.team_one_buy = "full-awp"
                elif self.game.game_information.team_one_money >= (cost_to_full):
                    self.game.game_information.team_one_money -= cost_to_full
                    self.game.game_information.team_one_buy = "full"
                else:
                    self.game.game_information.team_one_money -= cost_to_force
                    self.game.game_information.team_one_buy = "force"
        else:
            if self.game.game_information.team_one_money >= 30000:
                self.game.game_information.team_one_money -= 30000
                self.game.game_information.team_one_buy = "full-awp"
            elif self.game.game_information.team_one_money >= 25000:
                self.game.game_information.team_one_money -= 25000
                self.game.game_information.team_one_buy = "full"
            elif (
                self.game.game_information.team_one_money >= 12500
                and self.game.game_information.team_one_lossbonus >= 3
            ):
                self.game.game_information.team_one_money -= 12500
                self.game.game_information.team_one_buy = "force"
            else:
                self.game.game_information.team_one_buy = "save"

    def team_two_purchase(self) -> None:
        if self.game.game_information.team_two_surviving != 0:
            last_round_buy = self.game.game_information.team_two_buy

            if last_round_buy == "save":
                self.game.game_information.team_two_money -= 12500 - (
                    800 * self.game.game_information.team_two_surviving
                )
                self.game.game_information.team_two_buy = "force"
            else:
                money_per_survivor = 0

                if last_round_buy == "force":
                    money_per_survivor = 3750
                elif last_round_buy == "full":
                    money_per_survivor = 5000
                elif last_round_buy == "full-awp":
                    money_per_survivor = 6000

                cost_to_full_awp = 30000 - (
                    money_per_survivor * self.game.game_information.team_two_surviving
                )

                cost_to_full = 25000 - (
                    money_per_survivor * self.game.game_information.team_two_surviving
                )

                cost_to_force = 12500 - (
                    money_per_survivor * self.game.game_information.team_two_surviving
                )

                if self.game.game_information.team_two_money >= (cost_to_full_awp):
                    self.game.game_information.team_two_money -= cost_to_full_awp
                    self.game.game_information.team_two_buy = "full-awp"
                elif self.game.game_information.team_two_money >= (cost_to_full):
                    self.game.game_information.team_two_money -= cost_to_full
                    self.game.game_information.team_two_buy = "full"
                else:
                    self.game.game_information.team_two_money -= cost_to_force
                    self.game.game_information.team_two_buy = "force"
        else:
            if self.game.game_information.team_two_money >= 30000:
                self.game.game_information.team_two_money -= 30000
                self.game.game_information.team_two_buy = "full-awp"
            elif self.game.game_information.team_two_money >= 25000:
                self.game.game_information.team_two_money -= 25000
                self.game.game_information.team_two_buy = "full"
            elif (
                self.game.game_information.team_two_money >= 12500
                and self.game.game_information.team_two_lossbonus >= 3
            ):
                self.game.game_information.team_two_money -= 12500
                self.game.game_information.team_two_buy = "force"
            else:
                self.game.game_information.team_two_buy = "save"

    # the logic in here is NOT solid, but it works for now
    def make_purchases(self) -> None:
        # pistol round
        if (
            self.game.game_information.current_round == 1
            or self.game.game_information.current_round == 16
        ):
            self.game.game_information.team_one_buy = "save"
            self.game.game_information.team_two_buy = "save"

            self.game.game_information.team_one_money = 0
            self.game.game_information.team_two_money = 0
        else:
            self.team_one_purchase()
            self.team_two_purchase()

    def setup_round(self) -> None:
        self.game.game_information.current_round += 1

        self.repopulate_alive_lists()
        self.update_economy()
        self.make_purchases()


    def select_team_one_player(self) -> Player:
        return random.choice(self.game.game_information.team_one_alive)
    
    def select_team_two_player(self) -> Player:
        return random.choice(self.game.game_information.team_two_alive)

    def simulate_round(self) -> None:
        if self.debug:
            print(f"Current Round: {self.game.game_information.current_round}")
            print(f"Team One Score: {self.game.game_information.team_one_score}")
            print(f"Team One Score: {self.game.game_information.team_two_score}")
            print()
            print(
                f"Team One Loss Bonus: {self.game.game_information.team_one_lossbonus}"
            )
            print(
                f"Team Two Loss Bonus: {self.game.game_information.team_two_lossbonus}"
            )
            print(f"Team One Buy: {self.game.game_information.team_one_buy}")
            print(f"Team Two Buy: {self.game.game_information.team_two_buy}")
            print()

        while True:
            player_one = self.select_team_one_player()
            player_two = self.select_team_two_player()

