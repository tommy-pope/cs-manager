from .game import Game, Team, GameInformation, GameStats

class GameEngine():
    def __init__(self) -> None:
        self.game = None

    # main entry point into the game simulation
    def play_game(self, team_one: Team, team_two: Team) -> Game:
        self.setup_game(team_one, team_two)
        self.simulate_game()

        return self.game
    
    # creates game object
    def setup_game(self, team_one: Team, team_two: Team) -> None:
        game_stats = GameStats().load_blank_stats(team_one, team_two)

        self.game = Game(team_one, team_two, GameInformation(), game_stats)


    def simulate_game(self) -> None:
        pass