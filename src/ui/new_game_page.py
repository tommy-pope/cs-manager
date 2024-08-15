import customtkinter as ctk
from math import ceil

from .ui_util import hover_button, dehover_button
from ..gamefuncs.db import GameDB

def create_team_info_page(event, db, frame, team):
    children = frame.winfo_children()

    for child in range(2, len(children)):
        children[child].destroy()

    team_info_box = ctk.CTkFrame(frame, width=1000, height=1000)
    team_info_box.grid_propagate(False)
    team_info_box.grid(row=1, column=1, pady=30)

    team_generic_info = ctk.CTkFrame(team_info_box, width=400, height=300)
    team_generic_info.grid_propagate(False)
    team_generic_info.grid(row=0, column=0, padx=15, pady=15)

    team_name = ctk.CTkLabel(team_generic_info, width=380, text=f"Team: {team.info.name}", font=("Arial", 30))
    team_name.grid(row=0, column=0, pady=5, padx=5)

    team_rank = ctk.CTkLabel(team_generic_info, width=380, text=f"World Rank: {team.info.world_rank}", font=("Arial", 30))
    team_rank.grid(row=1, column=0, pady=5, padx=5)

    team_region = ctk.CTkLabel(team_generic_info, width=380, text=f"Region: {team.info.continent.sname}", font=("Arial", 30))
    team_region.grid(row=2, column=0, pady=5, padx=5)

    team_budget = ctk.CTkLabel(team_generic_info, width=380, text=f"Total Budget: {team.info.budget}", font=("Arial", 30))
    team_budget.grid(row=3, column=0, pady=5, padx=5)

    team_wage_budget = ctk.CTkLabel(team_generic_info, width=380, text=f"Wage Budget: {team.info.salary_budget}", font=("Arial", 30))
    team_wage_budget.grid(row=4, column=0, pady=5, padx=5)

    team_transfer_budget = ctk.CTkLabel(team_generic_info, width=380, text=f"Transfer Budget: {team.info.transfer_budget}", font=("Arial", 30))
    team_transfer_budget.grid(row=5, column=0, pady=5, padx=5)

    team_players_info = ctk.CTkFrame(team_info_box, width=540, height=300)
    team_players_info.grid_propagate(False)
    team_players_info.grid(row=0, column=1, padx=15, pady=15)

    for idx, player in enumerate(team.info.players):
        row = ctk.CTkFrame(team_players_info, width=520, height=30)
        row.grid_propagate(False)
        row.grid(row=idx, column=0, pady=10, padx=10)

        player_name = ctk.CTkLabel(row, width=100, height=30, text=player.info.nickname, font=("Arial", 15))
        player_name.grid(row=0, column=0)

        player_age = ctk.CTkLabel(row, width=30, height=30, text=player.info.age, font=("Arial", 15))
        player_age.grid(row=0, column=1)

        player_nation = ctk.CTkLabel(row, width=50, height=30, text=player.info.nationality, font=("Arial", 15))
        player_nation.grid(row=0, column=2)

def create_team_list(event, db, frame, region):
    children = frame.winfo_children()

    for child in range(1, len(children)):
        children[child].destroy()

    team_listing_box = ctk.CTkFrame(frame, width=1000, height=1000)
    team_listing_box.grid(row=0, column=1, padx=(35, 0))

    total_rows = ceil(len(db.continents[region].teams) / 8)  

    for rowidx in range(total_rows):
        row = ctk.CTkFrame(team_listing_box, width=980, height=176)
        row.grid(row=rowidx, column=0, pady=10, padx=10)

        for i in range(8):
            team_idx = rowidx * 8 + i
            if team_idx >= len(db.continents[region].teams):
                break

            team_name = ctk.CTkLabel(row, width=150, text=db.continents[region].teams[team_idx].info.name, font=("Arial", 20))
            team_name.bind("<Button-1>", lambda event, t=db.continents[region].teams[team_idx]: create_team_info_page(event, db, frame, t))
            team_name.bind("<Enter>", lambda event, name=team_name: hover_button(event, name))
            team_name.bind("<Leave>", lambda event, name=team_name: dehover_button(event, name))
            team_name.grid(row=0, column=i, padx=10)

def create_newgame_page(event, ui):
    root_children = list(ui.root.winfo_children())

    for child in root_children:
        child.destroy()

    db = GameDB()
    db.setup_game()
    ui.db = db

    frame = ctk.CTkFrame(ui.root, width=1920, height=1080)
    frame.grid(row=0, column=0)

    region_selection_dropdown = ctk.CTkComboBox(frame, values=["EU", "NA", "SA", "ASIA"], state="readonly", command=lambda event: create_team_list(event, ui.db, frame, region_selection_dropdown.get()))
    region_selection_dropdown.grid(column=0, row=0, sticky="w")
    region_selection_dropdown.set("EU")

    # default team list
    create_team_list(None, ui.db, frame, "EU")


