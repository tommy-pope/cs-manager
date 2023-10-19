from .data.player.player import *
from .engine.game_engine import GameEngine
from .gamefuncs.db import GameDB


def main():
    db = GameDB()
    db.setup_game()

    event = db.events[-1]
    event.generate_matches(db)

    engine = GameEngine(debug=True)

    for match in event.matches:
        finished_game = engine.play_game(match.team_one, match.team_two)
        match.scores.extend([finished_game.game_information.team_one_score, finished_game.game_information.team_two_score])
        match.game_stats = finished_game.game_stats

        if finished_game.game_information.team_one_score > finished_game.game_information.team_two_score:
            match.winner = match.team_one
            match.event.eliminate_team(match.team_two)
        else:
            match.winner = match.team_two
            match.event.eliminate_team(match.team_one)
    
    return

    team_one = db.teams[0]
    team_two = db.teams[-1]

    print("Team One:")
    [print(x.attributes.overall) for x in team_one.info.players]
    print()

    print("Team Two:")
    [print(x.attributes.overall) for x in team_two.info.players]
    print()

    engine = GameEngine(debug=True)
    engine.play_game(team_one, team_two)