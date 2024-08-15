from .data.player.player import *
from .engine.game_engine import GameEngine
from .gamefuncs.db import GameDB
from .ui.ui import UI

import customtkinter as ctk


def main():

    db = GameDB()
    db.setup_game()
    app = UI(db)
    app.create_application()

    app.root.mainloop()
