from .rankings_page import create_main_rankings
from .event_list_page import create_events_page
from .new_game_page import create_newgame_page

from .ui_util import hover_button, dehover_button

import customtkinter as ctk


class UI:
    def __init__(self, db) -> None:
        self.root = None
        self.db = db

        self.advance_button = None

    def create_application(self) -> ctk.CTk:
        ctk.set_appearance_mode("dark")

        app = ctk.CTk()
        app.geometry("1920x1080")
        self.root = app

        self.create_sidenavbar()
        self.create_mainpage()

    def create_main_menu(self):
        frame = ctk.CTkFrame(self.root, width=1920, height=1080)
        frame.grid(row=0, column=0)

        new_game = ctk.CTkLabel(frame, width=200, height=50, font=("Arial", 35), text="New Game")
        new_game.bind("<Button-1>", lambda event: create_newgame_page(event, self))
        new_game.bind("<Enter>", lambda event: hover_button(event, new_game))
        new_game.bind("<Leave>", lambda event: dehover_button(event, new_game))
        new_game.grid(row=0, column=0)

        load_game = ctk.CTkLabel(frame, width=200, height=50, font=("Arial", 35), text="Load Game")
        load_game.bind("<Enter>", lambda event: hover_button(event, load_game))
        load_game.bind("<Leave>", lambda event: dehover_button(event, load_game))
        load_game.grid(row=1, column=0)

    def advance_button_dropdown(self):
        advance_day_button = ctk.CTkButton(
            master=self.advance_button, text="Advance Day", command=lambda: self.db.advance(self, 1)
        )
        advance_day_button.grid(row=0, column=0, pady=5, padx=10)

        advance_week_button = ctk.CTkButton(
            master=self.advance_button, text="Advance Week", command=lambda: self.db.advance(self, 7)
        )
        advance_week_button.grid(row=1, column=0, pady=5, padx=10)

        advance_month_button = ctk.CTkButton(
            master=self.advance_button, text="Advance Month", command=lambda: self.db.advance(self, 31)
        )
        advance_month_button.grid(row=2, column=0, pady=5, padx=10)

    def create_sidenavbar(self):
        frame = ctk.CTkFrame(self.root, bg_color="gray", width=1000, height=1080)
        frame.grid(row=0, column=0, sticky="n")

        date_label = ctk.CTkLabel(
            master=frame,
            text=f"{self.db.date[0]}/{self.db.date[1]}/{self.db.date[2]}",
            width=200,
        )
        date_label.grid(row=0, column=0, pady=10, padx=10)

        advance_button = ctk.CTkButton(
            master=frame, text="Advance", command=lambda: self.advance_button_dropdown()
        )
        advance_button.grid(row=1, column=0, pady=10, padx=10)

        self.advance_button = advance_button

        ranking_button = ctk.CTkButton(
            master=frame, text="Rankings", command=lambda: create_main_rankings(self)
        )
        ranking_button.grid(row=2, column=0, pady=10, padx=10)

        events_button = ctk.CTkButton(
            master=frame,
            text="Events",
            command=lambda: create_events_page(self, "Upcoming"),
        )
        events_button.grid(row=3, column=0, pady=10, padx=10)

    def create_mainpage(self):
        frame = ctk.CTkFrame(self.root, width=1720, height=1080)
        frame.grid(row=0, column=1)

    def update_date(self):
        root_children = list(self.root.children.values())
        sidenav_children = list(root_children[0].children.values())
        date_label = sidenav_children[1]

        date_label.configure(
            text=f"{self.db.date[0]}/{self.db.date[1]}/{self.db.date[2]}"
        )