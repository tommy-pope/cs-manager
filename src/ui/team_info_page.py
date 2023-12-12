import customtkinter as ctk


def create_team_info_page(x, ui, team):
    root_children = list(ui.root.winfo_children())
    mainpage_children = list(root_children[1].winfo_children())

    for child in mainpage_children:
        child.destroy()

    root_frame = root_children[1]

    # main header
    team_header = ctk.CTkLabel(
        master=root_frame, text=f"{team.info.name}", font=("Arial", 35), width=1720
    )
    team_header.grid(row=0, column=0, columnspan=3, sticky="n", pady=10)

    # team information
    team_info_header = ctk.CTkLabel(
        master=root_frame, text="Team Information:", font=("Arial", 25)
    )
    team_info_header.grid(row=1, column=0, pady=10)

    team_info_box = ctk.CTkFrame(master=root_frame, width=500)
    team_info_box.grid(row=2, column=0)
    team_info_box.grid_propagate(False)

    team_name_info = ctk.CTkLabel(
        master=team_info_box,
        text=f"Team Name: {team.info.name}",
        font=("Arial", 15),
        width=500,
    )
    team_name_info.grid(row=0, column=0, sticky="n", pady=(10, 0))

    team_region_info = ctk.CTkLabel(
        master=team_info_box,
        text=f"Region: {team.info.continent.name}",
        font=("Arial", 15),
        width=500,
    )
    team_region_info.grid(row=1, column=0, sticky="n")

    team_ranking_info = ctk.CTkLabel(
        master=team_info_box,
        text=f"World Rank: {team.info.world_rank}",
        font=("Arial", 15),
        width=500,
    )
    team_ranking_info.grid(row=2, column=0, sticky="n")

    # team players
    team_players_header = ctk.CTkLabel(
        master=root_frame, text="Team Players:", font=("Arial", 25)
    )
    team_players_header.grid(row=1, column=1, pady=10)

    team_players_box = ctk.CTkFrame(master=root_frame, width=1020)
    team_players_box.grid(row=2, column=1)
    team_players_box.grid_propagate(False)

    table_header_row = ctk.CTkFrame(master=team_players_box)
    table_header_row.grid(row=0, column=0, pady=(10,), padx=(10,))

    player_name_header = ctk.CTkLabel(
        master=table_header_row, width=100, text="Nickname"
    )
    player_name_header.grid(row=0, column=0)

    player_age_header = ctk.CTkLabel(master=table_header_row, width=100, text="Age")
    player_age_header.grid(row=0, column=1)

    player_nationality_header = ctk.CTkLabel(
        master=table_header_row, width=100, text="Nation"
    )
    player_nationality_header.grid(row=0, column=2)

    player_overall_header = ctk.CTkLabel(
        master=table_header_row, width=100, text="Overall"
    )
    player_overall_header.grid(row=0, column=3)

    player_rifle_header = ctk.CTkLabel(master=table_header_row, width=100, text="Rifle")
    player_rifle_header.grid(row=0, column=4)

    player_awp_header = ctk.CTkLabel(master=table_header_row, width=100, text="AWP")
    player_awp_header.grid(row=0, column=5)

    player_pistol_header = ctk.CTkLabel(
        master=table_header_row, width=100, text="Pistol"
    )
    player_pistol_header.grid(row=0, column=6)

    player_positioning_header = ctk.CTkLabel(
        master=table_header_row, width=100, text="Positioning"
    )
    player_positioning_header.grid(row=0, column=7)

    player_clutch_header = ctk.CTkLabel(
        master=table_header_row, width=100, text="Clutch"
    )
    player_clutch_header.grid(row=0, column=8)

    player_consistency_header = ctk.CTkLabel(
        master=table_header_row, width=100, text="Consistency"
    )
    player_consistency_header.grid(row=0, column=9)

    for i, player in enumerate(team.info.players):
        row_frame = ctk.CTkFrame(master=team_players_box)
        row_frame.grid(row=i + 1, column=0, padx=(10,))

        player_name = ctk.CTkLabel(
            master=row_frame, width=100, text=player.info.nickname
        )
        player_name.grid(row=0, column=0)

        player_age = ctk.CTkLabel(master=row_frame, width=100, text=player.info.age)
        player_age.grid(row=0, column=1)

        player_nationality = ctk.CTkLabel(
            master=row_frame, width=100, text=player.info.nationality
        )
        player_nationality.grid(row=0, column=2)

        player_overall = ctk.CTkLabel(
            master=row_frame, width=100, text=round(player.attributes.overall)
        )
        player_overall.grid(row=0, column=3)

        player_rifle = ctk.CTkLabel(
            master=row_frame, width=100, text=round(player.attributes.rifle)
        )
        player_rifle.grid(row=0, column=4)

        player_awp = ctk.CTkLabel(
            master=row_frame, width=100, text=round(player.attributes.awp)
        )
        player_awp.grid(row=0, column=5)

        player_pistol = ctk.CTkLabel(
            master=row_frame, width=100, text=round(player.attributes.pistol)
        )
        player_pistol.grid(row=0, column=6)

        player_positioning = ctk.CTkLabel(
            master=row_frame, width=100, text=round(player.attributes.positioning)
        )
        player_positioning.grid(row=0, column=7)

        player_clutch = ctk.CTkLabel(
            master=row_frame, width=100, text=round(player.attributes.clutch)
        )
        player_clutch.grid(row=0, column=8)

        player_consistency = ctk.CTkLabel(
            master=row_frame, width=100, text=round(player.attributes.consistency)
        )
        player_consistency.grid(row=0, column=9)

    # recent events header
    team_events_header = ctk.CTkLabel(master=root_frame, text="Recent Events:", width=600, font=("Arial", 25))
    team_events_header.grid(row=3, column=0, pady=(10,0))

    # team recent events placements
    team_info_box = ctk.CTkFrame(master=root_frame, width=600)
    team_info_box.grid(row=4, column=0)
    team_info_box.grid_propagate(False)

    row = ctk.CTkFrame(master=team_info_box, width=600)
    row.grid(row=0, column=0)

    date_header = ctk.CTkLabel(master=row, text="Date:", width=200)
    date_header.grid(row=0, column=0)

    event_header = ctk.CTkLabel(master=row, text="Event:", width=250)
    event_header.grid(row=0, column=1)

    placement_header = ctk.CTkLabel(master=row, text="Placement:", width=150)
    placement_header.grid(row=0, column=2)

    all_events = team.events + team.past_events
    events_length = len(all_events) if len(all_events) < 10 else 10

    for i in range(events_length):
        event = all_events[i]
        row = ctk.CTkFrame(master=team_info_box, width=590)
        row.grid(row=i+1, column=0, pady=(5,0), padx=(5,5))

        date = ctk.CTkLabel(master=row, text=f"{event.start_date[0]}/{event.start_date[1]}/{event.start_date[2]}", width=200)
        date.grid(row=0, column=0)

        event_header = ctk.CTkLabel(master=row, text=event.name, width=250)
        event_header.grid(row=0, column=1)

        placement_header = ctk.CTkLabel(master=row, text="placeholder", width=140)
        placement_header.grid(row=0, column=2)






