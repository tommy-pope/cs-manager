from .data.player.player import *
from .engine.game_engine import GameEngine
from .gamefuncs.db import GameDB


def main():
    db = GameDB()
    db.setup_game()

    while True:
        print()
        print(f"Today's Date: {db.date[0]}/{db.date[1]}/{db.date[2]}")
        print()
        print("Options: ")
        print("1. Advance")
        print("2. Show Upcoming Events")
        print("3. Show Team Rankings")

        option = int(input())

        if option == 1:
            db.advance()
        elif option == 2:
            print()
            print("All Events:")
            for event in db.events:
                print()
                print(f"id: {event.id} name: {event.name} rep: {event.rep} start_date: {event.start_date} type: {event.type} continent: {event.continent}")
        elif option == 3:
            print()

            for idx, team in enumerate(db.teams):
                print()
                print(f"{idx+1}. id: {team.info.id} name: {team.info.name} rep: {team.info.reputation} cont: {team.info.continent.sname}")
        