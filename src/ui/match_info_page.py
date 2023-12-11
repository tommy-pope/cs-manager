import customtkinter as ctk

from .team_info_page import create_team_info_page

def create_match_info_page(x, ui, match, selected_map_idx):
    root_children = list(ui.root.winfo_children())
    mainpage_children = list(root_children[1].winfo_children())

    for child in mainpage_children:
        child.destroy()

    root_frame = root_children[1]

    # determines what to put as score
    if len(match.scores) == 0:
        team_one_score = 0
        team_two_score = 0
    else:
        if match.bo == 1:
            team_one_score = match.scores[0][0]
            team_two_score = match.scores[0][1]
        else:
            team_one_score = 0
            team_two_score = 0

            for score in match.scores:
                if score[0] > score[1]:
                    team_one_score += 1
                else:
                    team_two_score += 1

    # match header
    team_one_header = ctk.CTkLabel(master=root_frame, text=f"{match.team_one.info.name} - {team_one_score}", font=("Arial", 40), width=1720/2, height=200, anchor="e")
    team_one_header.grid(row=0, column=0, padx=(0,20))
    team_one_header.bind("<Button-1>", lambda x, copy=match.team_one: create_team_info_page(x, ui, copy))

    team_two_header = ctk.CTkLabel(master=root_frame, text=f"{team_two_score} - {match.team_two.info.name}", font=("Arial", 40), width=1720/2, height=200, anchor="w")
    team_two_header.grid(row=0, column=1, padx=(20,0))
    team_two_header.bind("<Button-1>", lambda x, copy=match.team_two: create_team_info_page(x, ui, copy))

    row_idx = 1

    # map selector
    if match.bo > 1:
        row_idx += 1

        map_selector = ctk.CTkFrame(master=root_frame, width=1720)
        map_selector.grid(row=1, column=0, columnspan=2)

        for i in range(len(match.scores)):
            map_option = ctk.CTkButton(master=map_selector, text=f"Map {i+1}", command=lambda copy=i: create_match_info_page(None, ui, match, copy))
            map_option.grid(row=0, column=i)
        
    # map score
    map_score = ctk.CTkLabel(master=root_frame, text=f"Map {selected_map_idx+1}: {match.scores[selected_map_idx][0]} - {match.scores[selected_map_idx][1]}", font=("Arial", 40), width=1720/2, height=100)
    map_score.grid(row=row_idx, column=0, columnspan=2)

    team_one_stats = match.game_stats[selected_map_idx].team_one_stats
    team_two_stats = match.game_stats[selected_map_idx].team_two_stats

    for i in range(2):
        stats = team_one_stats if i == 0 else team_two_stats

        stats_frame = ctk.CTkFrame(master=root_frame, width=1720/2)
        stats_frame.grid(row=row_idx+1, column=i)

        # header row
        row = ctk.CTkFrame(master=stats_frame)
        row.grid(row=0, column=0)

        name_header = ctk.CTkLabel(master=row, text="Name:", width=100, anchor="w", font=("Arial", 20))
        name_header.grid(row=0, column=0)

        kill_header = ctk.CTkLabel(master=row, text="Kills:", width=100, anchor="w", font=("Arial", 20))
        kill_header.grid(row=0, column=1)

        assist_header = ctk.CTkLabel(master=row, text="Assists:", width=100, anchor="w", font=("Arial", 20))
        assist_header.grid(row=0, column=2)

        death_header = ctk.CTkLabel(master=row, text="Deaths:", width=100, anchor="w", font=("Arial", 20))
        death_header.grid(row=0, column=3)

        adr_header = ctk.CTkLabel(master=row, text="ADR:", width=100, anchor="w", font=("Arial", 20))
        adr_header.grid(row=0, column=4)

        rating_header = ctk.CTkLabel(master=row, text="Rating:", width=100, anchor="w", font=("Arial", 20))
        rating_header.grid(row=0, column=5)

        for x, key in enumerate(stats):
            row = ctk.CTkFrame(master=stats_frame)
            row.grid(row=x+1, column=0)

            player_name = ctk.CTkLabel(master=row, text=key, width=100, anchor="w", font=("Arial", 15))
            player_name.grid(row=0, column=0)

            player_kills = ctk.CTkLabel(master=row, text=stats[key]["kills"], width=100, anchor="w", font=("Arial", 15))
            player_kills.grid(row=0, column=1)

            player_assists = ctk.CTkLabel(master=row, text=stats[key]["assists"], width=100, anchor="w", font=("Arial", 15))
            player_assists.grid(row=0, column=2)

            player_deaths = ctk.CTkLabel(master=row, text=stats[key]["deaths"], width=100, anchor="w", font=("Arial", 15))
            player_deaths.grid(row=0, column=3)

            player_adr = ctk.CTkLabel(master=row, text=stats[key]["adr"], width=100, anchor="w", font=("Arial", 15))
            player_adr.grid(row=0, column=4)

            player_rating = ctk.CTkLabel(master=row, text=stats[key]["rating"], width=100, anchor="w", font=("Arial", 15))
            player_rating.grid(row=0, column=5)