import customtkinter as ctk

def create_main_rankings(ui):
    root_children = list(ui.root.winfo_children())
    mainpage_children = list(root_children[1].winfo_children())

    for child in mainpage_children:
        child.destroy()

    root_frame = root_children[1]

    # main header
    ranking_header = ctk.CTkLabel(master=root_frame, text=f"World Rankings", font=("Arial", 35), width=1720)
    ranking_header.grid(row=0, column=0, columnspan=5, sticky="n", pady=10)

    # ranking region selector

    ranking_region = ctk.CTkFrame(root_frame, width=200)
    ranking_region.grid(row=1, column=0, padx=50)

    world_rankings = ctk.CTkButton(master=ranking_region, text="World", command=lambda: create_main_rankings(ui))
    world_rankings.grid(row=0, column=0)

    eu_rankings = ctk.CTkButton(master=ranking_region, text="Europe", command=lambda: create_region_rankings(ui, "EU"))
    eu_rankings.grid(row=1, column=0)

    na_rankings = ctk.CTkButton(master=ranking_region, text="North America", command=lambda: create_region_rankings(ui, "NA"))
    na_rankings.grid(row=2, column=0)

    sa_rankings = ctk.CTkButton(master=ranking_region, text="South America", command=lambda: create_region_rankings(ui, "SA"))
    sa_rankings.grid(row=3, column=0)

    asia_rankings = ctk.CTkButton(master=ranking_region, text="Asia", command=lambda: create_region_rankings(ui, "ASIA"))
    asia_rankings.grid(row=4, column=0)

    # ranking table

    ranking_table = ctk.CTkFrame(root_frame)
    ranking_table.grid(row=1, column=1, columnspan=4, sticky="w", pady=25)

    header_row = ctk.CTkFrame(ranking_table)
    header_row.grid(row=0, column=0, columnspan=3)

    rank_header = ctk.CTkLabel(header_row, text="Rank", width=100, anchor="w", font=("Arial", 25))
    rank_header.grid(row=0, column=0)

    name_header = ctk.CTkLabel(header_row, text="Team", width=175, anchor="w", font=("Arial", 25))
    name_header.grid(row=0, column=1)

    region_header = ctk.CTkLabel(header_row, text="Region", width=125, anchor="w", font=("Arial", 25))
    region_header.grid(row=0, column=2)

    elo_header = ctk.CTkLabel(header_row, text="ELO", width=100, anchor="w", font=("Arial", 25))
    elo_header.grid(row=0, column=3)


    for i in range(30):
        row = ctk.CTkFrame(ranking_table)
        row.grid(row=i+1, column=0)

        team_rank = f"{i + 1}."
        team_name = ui.db.teams[i].info.name
        team_region = ui.db.teams[i].info.continent.sname
        team_elo = ui.db.teams[i].info.elo
        
        rank_widget = ctk.CTkLabel(row, text=team_rank, width=100, anchor="w", font=("Arial", 15))
        rank_widget.grid(row=0, column=0)

        name_widget = ctk.CTkLabel(row, text=team_name, width=175, anchor="w", font=("Arial", 15))
        name_widget.grid(row=0, column=1)

        region_widget = ctk.CTkLabel(row, text=team_region, width=125, anchor="w", font=("Arial", 15))
        region_widget.grid(row=0, column=2)

        elo_widget = ctk.CTkLabel(row, text=team_elo, width=100, anchor="w", font=("Arial", 15))
        elo_widget.grid(row=0, column=3)

def create_region_rankings(ui, region):
    root_children = list(ui.root.winfo_children())
    mainpage_children = list(root_children[1].winfo_children())

    for child in mainpage_children:
        child.destroy()

    root_frame = root_children[1]

    # main header
    ranking_header = ctk.CTkLabel(master=root_frame, text=f"{region} Rankings", font=("Arial", 35), width=1720)
    ranking_header.grid(row=0, column=0, columnspan=5, sticky="n", pady=10)

    # ranking region selector

    ranking_region = ctk.CTkFrame(root_frame)
    ranking_region.grid(row=1, column=0, padx=50)

    world_rankings = ctk.CTkButton(master=ranking_region, text="World", command=lambda: create_main_rankings(ui))
    world_rankings.grid(row=0, column=0)

    eu_rankings = ctk.CTkButton(master=ranking_region, text="Europe", command=lambda: create_region_rankings(ui, "EU"))
    eu_rankings.grid(row=1, column=0)

    na_rankings = ctk.CTkButton(master=ranking_region, text="North America", command=lambda: create_region_rankings(ui, "NA"))
    na_rankings.grid(row=2, column=0)

    sa_rankings = ctk.CTkButton(master=ranking_region, text="South America", command=lambda: create_region_rankings(ui, "SA"))
    sa_rankings.grid(row=3, column=0)

    asia_rankings = ctk.CTkButton(master=ranking_region, text="Asia", command=lambda: create_region_rankings(ui, "ASIA"))
    asia_rankings.grid(row=4, column=0)

    # ranking table

    ranking_table = ctk.CTkFrame(root_frame)
    ranking_table.grid(row=1, column=1, columnspan=4, sticky="w", pady=25)

    header_row = ctk.CTkFrame(ranking_table)
    header_row.grid(row=0, column=0, columnspan=3)

    rank_header = ctk.CTkLabel(header_row, text="Rank", width=100, anchor="w", font=("Arial", 25))
    rank_header.grid(row=0, column=0)

    name_header = ctk.CTkLabel(header_row, text="Team", width=175, anchor="w", font=("Arial", 25))
    name_header.grid(row=0, column=1)

    region_header = ctk.CTkLabel(header_row, text="Region", width=125, anchor="w", font=("Arial", 25))
    region_header.grid(row=0, column=2)

    elo_header = ctk.CTkLabel(header_row, text="ELO", width=100, anchor="w", font=("Arial", 25))
    elo_header.grid(row=0, column=3)

    region_teams = ui.db.continents[region].teams
    num_teams = len(region_teams) if len(region_teams) < 30 else 30

    for i in range(num_teams):
        row = ctk.CTkFrame(ranking_table)
        row.grid(row=i+1, column=0)

        team_rank = f"{i + 1}."
        team_name = region_teams[i].info.name
        team_region = region_teams[i].info.continent.sname
        team_elo = region_teams[i].info.elo
        
        rank_widget = ctk.CTkLabel(row, text=team_rank, width=100, anchor="w", font=("Arial", 15))
        rank_widget.grid(row=0, column=0)

        name_widget = ctk.CTkLabel(row, text=team_name, width=175, anchor="w", font=("Arial", 15))
        name_widget.grid(row=0, column=1)

        region_widget = ctk.CTkLabel(row, text=team_region, width=125, anchor="w", font=("Arial", 15))
        region_widget.grid(row=0, column=2)

        elo_widget = ctk.CTkLabel(row, text=team_elo, width=100, anchor="w", font=("Arial", 15))
        elo_widget.grid(row=0, column=3)
