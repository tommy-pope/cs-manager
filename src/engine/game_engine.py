import copy
import random

from .weapon_stats import weapon_stats

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

            # make copies of players for game
            self.game.game_information.team_one_alive = copy.deepcopy(
                self.game.team_one.info.players
            )
            
            self.game.game_information.team_two_alive = copy.deepcopy(
                self.game.team_two.info.players
            )

            self.setup_round()
            self.simulate_round()

    def repopulate_alive_lists(self) -> None:
        for player in self.game.game_information.team_one_alive:
            player.hp = 100
            player.alive = True
            player.hit_by = []

        for player in self.game.game_information.team_two_alive:
            player.hp = 100
            player.alive = True
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

            self.game.game_information.team_one_lossbonus = 1
            self.game.game_information.team_two_lossbonus = 1

            self.game.game_information.team_one_surviving = 0
            self.game.game_information.team_two_surviving = 0

    def team_one_purchase(self) -> None:
        if self.game.game_information.team_one_surviving != 0:
            last_round_buy = self.game.game_information.team_one_buy

            money_per_survivor = 0

            if last_round_buy == "save":
                money_per_survivor = 800
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
                self.game.game_information.team_one_money >= 23000
                and self.game.game_information.team_one_lossbonus >= 4
            ):
                self.game.game_information.team_one_money -= 12500
                self.game.game_information.team_one_buy = "force"
            else:
                self.game.game_information.team_one_buy = "save"

    def team_two_purchase(self) -> None:
        if self.game.game_information.team_two_surviving != 0:
            last_round_buy = self.game.game_information.team_two_buy

            money_per_survivor = 0
                
            if last_round_buy == "save":
                money_per_survivor = 800
            elif last_round_buy == "force":
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
                self.game.game_information.team_two_money >= 23000
                and self.game.game_information.team_two_lossbonus >= 4
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

        print(f"Team One Money: {self.game.game_information.team_one_money}")
        print(f"Team Two Money: {self.game.game_information.team_two_money}")

        self.make_purchases()

        print(f"Team One Money: {self.game.game_information.team_one_money}")
        print(f"Team Two Money: {self.game.game_information.team_two_money}")


    def select_team_one_player(self) -> Player:
        valid_players = [player for player in self.game.game_information.team_one_alive if player.alive == True]

        return random.choice(valid_players)
    
    def select_team_two_player(self) -> Player:
        valid_players = [player for player in self.game.game_information.team_two_alive if player.alive == True]

        return random.choice(valid_players)

    def calculate_buy_odds(self, player_one_is_awp: bool, player_two_is_awp: bool) -> int:
        team_one_buy = self.game.game_information.team_one_buy
        team_two_buy = self.game.game_information.team_two_buy

        if not player_one_is_awp and team_one_buy == "full-awp":
            team_one_buy = "full"

        if not player_two_is_awp and team_two_buy == "full-awp":
            team_two_buy = "full"

        return weapon_stats[team_one_buy][team_two_buy]

    def calculate_encounter_odds(self, player_one: Player, player_two: Player) -> float:
        # larger number favors player one, smaller favors player two
        buy_odds = self.calculate_buy_odds(player_one.attributes.is_awper, player_two.attributes.is_awper)

        odds = 50 + (buy_odds)

        return odds

    def team_one_round_win(self, team_one_players_alive: int) -> None:
        self.game.game_information.team_one_score += 1
        self.game.game_information.last_round_winner = 1

        self.game.game_information.team_one_surviving = team_one_players_alive
        self.game.game_information.team_two_surviving = 0

    def team_two_round_win(self, team_two_players_alive: int) -> None:
        self.game.game_information.team_two_score += 1
        self.game.game_information.last_round_winner = 2

        self.game.game_information.team_two_surviving = team_two_players_alive
        self.game.game_information.team_one_surviving = 0

        print()
        print(f"Team Two won with {team_two_players_alive} alive.")

    def simulate_round(self) -> None:
        team_one_players_alive = 5
        team_two_players_alive = 5

        while team_one_players_alive != 0 and team_two_players_alive != 0:
            player_one = self.select_team_one_player()
            player_two = self.select_team_two_player()

            odds = self.calculate_encounter_odds(player_one, player_two)

            if (random.random() * 100) < odds:
                player_two.hp = 0
                player_two.alive = False
                team_two_players_alive -= 1
            else:
                player_one.hp = 0
                player_one.alive = False
                team_one_players_alive -= 1

        # determine round winner
        if team_one_players_alive == 0:
            self.team_two_round_win(team_two_players_alive)
        elif team_two_players_alive == 0:
            self.team_one_round_win(team_one_players_alive)
            
        if self.debug:
            print()
            print(f"Current Round: {self.game.game_information.current_round}")
            print(f"Team One Score: {self.game.game_information.team_one_score}")
            print(f"Team Two Score: {self.game.game_information.team_two_score}")
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
        
        if self.game.game_information.team_one_score == 15 and self.game.game_information.team_two_score == 15:
            self.game.game_information.is_overtime = True



