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

        option = int(input())

        if option == 1:
            db.advance()