import copy
import random

from .weapon_stats import weapon_stats

from .game import Game, Team, GameInformation, GameStats
from ..data.player.player import Player, PlayerAttributes


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
        game_stats = GameStats()
        game_stats.load_blank_stats(team_one, team_two)

        self.game = Game(team_one, team_two, GameInformation(), game_stats)

    def simulate_game(self) -> None:
        # while the score of both teams is less than 16, and it is not 15-15
        while (
            self.game.game_information.team_one_score < self.game.game_information.rounds_to_reach
            and self.game.game_information.team_two_score < self.game.game_information.rounds_to_reach
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

        self.calculate_postgame_stats()

    def calculate_postgame_stats(self) -> None:
        rounds = self.game.game_information.current_round

        for player in self.game.team_one.info.players:
            self.game.game_stats.team_one_stats[player.info.player_id]["fpr"] = round(self.game.game_stats.team_one_stats[player.info.player_id]["kills"]/rounds, 2)
            self.game.game_stats.team_one_stats[player.info.player_id]["apr"] = round(self.game.game_stats.team_one_stats[player.info.player_id]["assists"]/rounds, 2)
            self.game.game_stats.team_one_stats[player.info.player_id]["fbpr"] = round(self.game.game_stats.team_one_stats[player.info.player_id]["first_bloods"]/rounds, 2)
            self.game.game_stats.team_one_stats[player.info.player_id]["cpr"] = round(self.game.game_stats.team_one_stats[player.info.player_id]["clutches"]/rounds, 2)
            self.game.game_stats.team_one_stats[player.info.player_id]["mkpr"] = round(self.game.game_stats.team_one_stats[player.info.player_id]["multikills"]/rounds, 2)
            self.game.game_stats.team_one_stats[player.info.player_id]["adr"] = round(self.game.game_stats.team_one_stats[player.info.player_id]["damage"]/rounds, 2)

            self.game.game_stats.team_one_stats[player.info.player_id]["rating"] = self.calculate_player_rating(player, self.game.game_stats.team_one_stats)

        for player in self.game.team_two.info.players:
            self.game.game_stats.team_two_stats[player.info.player_id]["fpr"] = round(self.game.game_stats.team_two_stats[player.info.player_id]["kills"]/rounds, 2)
            self.game.game_stats.team_two_stats[player.info.player_id]["apr"] = round(self.game.game_stats.team_two_stats[player.info.player_id]["assists"]/rounds, 2)
            self.game.game_stats.team_two_stats[player.info.player_id]["fbpr"] = round(self.game.game_stats.team_two_stats[player.info.player_id]["first_bloods"]/rounds, 2)
            self.game.game_stats.team_two_stats[player.info.player_id]["cpr"] = round(self.game.game_stats.team_two_stats[player.info.player_id]["clutches"]/rounds, 2)
            self.game.game_stats.team_two_stats[player.info.player_id]["mkpr"] = round(self.game.game_stats.team_two_stats[player.info.player_id]["multikills"]/rounds, 2)
            self.game.game_stats.team_two_stats[player.info.player_id]["adr"] = round(self.game.game_stats.team_two_stats[player.info.player_id]["damage"]/rounds, 2)

            self.game.game_stats.team_two_stats[player.info.player_id]["rating"] = self.calculate_player_rating(player, self.game.game_stats.team_two_stats)

            
        for item in self.game.game_stats.team_one_stats.items():
            print(item)

        for item in self.game.game_stats.team_two_stats.items():
            print(item)

    def calculate_player_rating(self, player: Player, stats: GameStats) -> float:
        fpr_adj = .3
        apr_adj = .9
        fbpr_adj = .9

        cpr_adj = .9
        cpr_scale = 5

        mkpr_adj = .9

        adr_adj = 35
        adr_scale = 100

        fpr = stats[player.info.player_id]["fpr"] + fpr_adj
        apr = stats[player.info.player_id]["apr"] + apr_adj
        fbpr = stats[player.info.player_id]["fbpr"] + fbpr_adj
        cpr = (stats[player.info.player_id]["cpr"] * cpr_scale) + cpr_adj
        mkpr = stats[player.info.player_id]["mkpr"] + mkpr_adj
        adr = (stats[player.info.player_id]["adr"] + adr_adj) / adr_scale

        fpr_weight = .25
        apr_weight = .15
        fbpr_weight = .2
        cpr_weight = .1
        mkpr_weight = .1
        adr_weight = .2
        
        return round((fpr * fpr_weight) + (apr * apr_weight) + (fbpr * fbpr_weight) + (cpr * cpr_weight) + (mkpr * mkpr_weight) + (adr * adr_weight), 2)


    def repopulate_alive_lists(self) -> None:
        for player in self.game.game_information.team_one_alive:
            player.hp = 100
            player.alive = True
            player.hit_by = []
            player.kills_in_round = 0

        for player in self.game.game_information.team_two_alive:
            player.hp = 100
            player.alive = True
            player.hit_by = []
            player.kills_in_round = 0

    def update_economy(self) -> None:
        # if not first round, or halftime
        if (
            (self.game.game_information.current_round != 1
            or self.game.game_information.current_round != 16)
            and not self.game.game_information.is_overtime
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
            starting_money = 80000 if self.game.game_information.is_overtime else 4000

            self.game.game_information.team_one_money = starting_money
            self.game.game_information.team_two_money = starting_money

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

    def calculate_stats_odds(self, player_one: PlayerAttributes, player_two: PlayerAttributes, team_one_alive: int, team_two_alive: int) -> float:
        team_one_buy = self.game.game_information.team_one_buy
        team_two_buy = self.game.game_information.team_two_buy

        if not player_one.is_awper and team_one_buy == "full-awp":
            team_one_buy = "full"

        if not player_two.is_awper and team_two_buy == "full-awp":
            team_two_buy = "full"

        player_one_stat = ""
        player_two_stat = ""

        player_one_stat = player_one.awp if player_one.is_awper and team_one_buy == "full-awp" else player_one_stat
        player_one_stat = player_one.rifle if not player_one.is_awper and team_one_buy == "full-awp" else player_one_stat
        player_one_stat = player_one.rifle if team_one_buy == "full" else player_one_stat
        player_one_stat = player_one.awp if team_one_buy == "force" and player_one.is_awper else player_one_stat
        player_one_stat = player_one.rifle if team_one_buy == "force" and not player_one.is_awper else player_one_stat
        player_one_stat = player_one.pistol if team_one_buy == "save" else player_one_stat

        player_two_stat = player_two.awp if player_two.is_awper and team_two_buy == "full-awp" else player_two_stat
        player_two_stat = player_two.rifle if not player_two.is_awper and team_two_buy == "full-awp" else player_two_stat
        player_two_stat = player_two.rifle if team_two_buy == "full" else player_two_stat
        player_two_stat = player_two.awp if team_two_buy == "force" and player_two.is_awper else player_two_stat
        player_two_stat = player_two.rifle if team_two_buy == "force" and not player_two.is_awper else player_two_stat
        player_two_stat = player_two.pistol if team_two_buy == "save" else player_two_stat

        skill_weight = .25
        con_weight = .15
        clu_weight = .1

        p1_clutch = player_one.clutch if team_one_alive == 1 else 0
        p2_clutch = player_two.clutch if team_two_alive == 1 else 0

        skill_odds = (player_one_stat - player_two_stat) * skill_weight
        con_odds = (player_one.consistency - player_two.consistency) * con_weight

        if team_one_alive == 1 and team_two_alive == 1:
            clu_odds = (p1_clutch - p2_clutch) * clu_weight
        elif team_one_alive == 1:
            clu_odds = (p1_clutch / 10) * clu_weight 
        elif team_two_alive == 1:
            clu_odds = -(p2_clutch / 10) * clu_weight
        else:
            clu_odds = 0


        return skill_odds + con_odds + clu_odds

    def calculate_encounter_odds(self, player_one: Player, player_two: Player, team_one_alive: int, team_two_alive: int) -> float:
        # larger number favors player one, smaller favors player two
        buy_odds = self.calculate_buy_odds(player_one.attributes.is_awper, player_two.attributes.is_awper)
        stats_odds = self.calculate_stats_odds(player_one.attributes, player_two.attributes, team_one_alive, team_two_alive)

        odds = 50 + buy_odds + stats_odds

        return odds

    def calculate_damage_done(self, player: Player, team_buy: str) -> int:
        player_stat = ""

        player_stat = "AWP" if player.attributes.is_awper and team_buy == "full-awp" else player_stat
        player_stat = "RIFLE" if not player.attributes.is_awper and team_buy == "full-awp" else player_stat
        player_stat = "RIFLE" if team_buy == "full" else player_stat
        player_stat = "AWP" if team_buy == "force" and player.attributes.is_awper else player_stat
        player_stat = "RIFLE" if team_buy == "force" and not player.attributes.is_awper else player_stat
        player_stat = "PISTOL" if team_buy == "save" else player_stat
        
        if player_stat == "AWP":
            chance_to_kill = 80 + (player.attributes.awp/10)
            min_damage = 50
        elif player_stat == "RIFLE":
            chance_to_kill = 65 + (player.attributes.rifle/10)
            min_damage = 20
        elif player_stat == "PISTOL":
            chance_to_kill = 60 + (player.attributes.pistol/10)
            min_damage = 10

        chance = random.random() * 100

        if chance < chance_to_kill:
            return 100
        else:
            return random.randint(min_damage, 99)

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

    def on_player_death(self, dead_player: Player, team: str) -> None:
        dead_player.hp = 0
        dead_player.alive = False
        
        if team == "team_one":
            self.game.game_stats.team_one_stats[dead_player.info.player_id]["deaths"] += 1
        elif team == "team_two":
            self.game.game_stats.team_two_stats[dead_player.info.player_id]["deaths"] += 1

        for player in dead_player.hit_by:
            if team == "team_one":
                self.game.game_stats.team_two_stats[player.info.player_id]["assists"] += 1
            elif team == "team_two":
                self.game.game_stats.team_one_stats[player.info.player_id]["assists"] += 1
            
    def simulate_round(self) -> None:
        team_one_players_alive = 5
        team_two_players_alive = 5

        while team_one_players_alive != 0 and team_two_players_alive != 0:
            player_one = self.select_team_one_player()
            player_two = self.select_team_two_player()

            odds = self.calculate_encounter_odds(player_one, player_two, team_one_players_alive, team_two_players_alive)

            if (random.random() * 100) < odds:
                damage = self.calculate_damage_done(player_one, self.game.game_information.team_one_buy)

                # killed them
                if damage >= player_two.hp:
                    # incase of damage overflow
                    damage = player_two.hp
                    self.on_player_death(player_two, "team_two")

                    team_two_players_alive -=1

                    self.game.game_stats.team_one_stats[player_one.info.player_id]["kills"] += 1
                    player_one.kills_in_round += 1

                    if player_one.kills_in_round == 2:
                        self.game.game_stats.team_one_stats[player_one.info.player_id]["multikills"] += 1

                    if team_two_players_alive == 4:
                        self.game.game_stats.team_one_stats[player_one.info.player_id]["first_bloods"] += 1
                    
                    if team_one_players_alive == 1 and team_two_players_alive == 0:
                        self.game.game_stats.team_one_stats[player_one.info.player_id]["clutches"] += 1
                else:
                    player_two.hp -= damage
                    if player_one not in player_two.hit_by:
                        player_two.hit_by.append(player_one)


                self.game.game_stats.team_one_stats[player_one.info.player_id]["damage"] += damage
            else:
                damage = self.calculate_damage_done(player_two, self.game.game_information.team_two_buy)

                # killed them
                if damage >= player_one.hp:
                    # incase of damage overflow
                    damage = player_one.hp

                    self.on_player_death(player_one, "team_one")
                    team_one_players_alive -= 1

                    self.game.game_stats.team_two_stats[player_two.info.player_id]["kills"] += 1
                    player_two.kills_in_round += 1

                    if player_two.kills_in_round == 2:
                        self.game.game_stats.team_two_stats[player_two.info.player_id]["multikills"] += 1

                    if team_one_players_alive == 4:
                        self.game.game_stats.team_two_stats[player_two.info.player_id]["first_bloods"] += 1
                    
                    if team_two_players_alive == 1 and team_one_players_alive == 0:
                        self.game.game_stats.team_two_stats[player_two.info.player_id]["clutches"] += 1
                else:
                    player_one.hp -= damage
                    if player_two not in player_one.hit_by:
                        player_one.hit_by.append(player_two)
                
                self.game.game_stats.team_two_stats[player_two.info.player_id]["damage"] += damage

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
        
        if self.game.game_information.team_one_score == self.game.game_information.rounds_to_reach-1 and self.game.game_information.team_two_score == self.game.game_information.rounds_to_reach-1:
            self.game.game_information.is_overtime = True
            self.game.game_information.rounds_to_reach += 3
