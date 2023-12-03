import customtkinter as ctk

def create_event_info_page(x, ui, event):
    root_children = list(ui.root.winfo_children())
    mainpage_children = list(root_children[1].winfo_children())

    for child in mainpage_children:
        child.destroy()

    root_frame = root_children[1]

    # main header
    event_header = ctk.CTkLabel(master=root_frame, text=f"{event.name}", font=("Arial", 35), width=1720)
    event_header.grid(row=0, column=0, columnspan=5, sticky="n", pady=10)

    # event information
    event_info_header = ctk.CTkLabel(master=root_frame, text="Event Information:", font=("Arial", 25))
    event_info_header.grid(row=1, column=1, pady=10)

    event_info_box = ctk.CTkFrame(master=root_frame, width=500)
    event_info_box.grid(row=2, column=1)

    event_dates_info = ctk.CTkLabel(master=event_info_box, text=f"Dates: {event.start_date[0]}/{event.start_date[1]}/{event.start_date[2]} - {event.end_date[0]}/{event.end_date[1]}/{event.end_date[2]}", font=("Arial", 15))
    event_dates_info.grid(row=0, column=0, sticky="n")

    event_types_info = ctk.CTkLabel(master=event_info_box, text=f"Reputation: {event.rep}", font=("Arial", 15))
    event_types_info.grid(row=1, column=0, sticky="n")

    event_regions_info = ctk.CTkLabel(master=event_info_box, text=f"Region: {event.continent}", font=("Arial", 15))
    event_regions_info.grid(row=2, column=0, sticky="n")

    event_num_teams_info = ctk.CTkLabel(master=event_info_box, text=f"Number of Teams: {len(event.teams)}", font=("Arial", 15))
    event_num_teams_info.grid(row=3, column=0, sticky="n")

    # event teams
    event_teams_header = ctk.CTkLabel(master=root_frame, text="Teams in Event:", font=("Arial", 25))
    event_teams_header.grid(row=1, column=2, pady=10)

    event_teams_box = ctk.CTkFrame(master=root_frame, width=1000)
    event_teams_box.grid(row=2, column=2)
    event_teams_box.grid_propagate(False)

    for i, team in enumerate(event.teams):
        event_team = ctk.CTkLabel(master=event_teams_box, text=f"{team.info.name} | {team.info.continent.sname}", font=("Arial", 20), width=200)
        event_team.grid(row=i // 5, column=i % 5, pady=5)

    if event.type == "qual":
        event_diagram_text = "Bracket:"
    elif event.type == "main":
        event_diagram_text = "Group Stage:"

    # event diagram
    event_matches_header = ctk.CTkLabel(master=root_frame, text=event_diagram_text, font=("Arial", 25))
    event_matches_header.grid(row=3, column=0, pady=10, columnspan=5)

    event_diagram_frame = ctk.CTkFrame(master=root_frame, width=1000, height=640)
    event_diagram_frame.grid(row=4, column=0, pady=10, columnspan=5)
    event_diagram_frame.grid_propagate(False)

    if event.type == "qual":
        matches_foreach_round = {i: None for i in range(1, event.total_rounds + 1)}

        # need to determine how many rounds there will be
        for round in range(1, event.total_rounds + 1):
            matches_in_round = [match for match in event.matches if match.round_in_event == round]

            round_frame = ctk.CTkFrame(master=event_diagram_frame, width=200, height=630)
            round_frame.grid(row=0, column=round-1, rowspan=9, pady=5)
            round_frame.grid_propagate(False)

            # if these games haven't been generated, then fake them
            if len(matches_in_round) == 0:
                # if not an even teams before, special case
                if round == 2:
                    fake_matches = int((len(event.teams) - len(matches_foreach_round[1]))/2)
                else:
                    fake_matches = int(len(matches_foreach_round[round-1])/2)
                    
                matches_in_round = [i for i in range(fake_matches)]
                    
            matches_foreach_round[round] = matches_in_round

            if len(matches_in_round) == 1:
                rows_with_matches = [4]
            elif len(matches_in_round) % 2 == 0:
                rows_with_matches = [0,1,2,3,4,5,6,7,8]
            else:
                rows_with_matches = [0,1,2,3,4,5,6,7,8]

            for i in range(9):
                match_frame = ctk.CTkFrame(master=round_frame, height=70)

                match_frame.grid(column=0, row=i)
                match_frame.grid_propagate(False)
                if i in rows_with_matches:
                    match_idx = rows_with_matches.index(i)

                    if match_idx > len(matches_in_round) - 1:
                        continue

                    if type(matches_in_round[match_idx]) != int:
                        team_one_text = matches_in_round[match_idx].team_one.info.name
                        team_two_text = matches_in_round[match_idx].team_two.info.name
                    else:
                        team_one_text = "TBD"
                        team_two_text = "TBD"

                    team_one_label = ctk.CTkLabel(master=match_frame, text=team_one_text, height=30)
                    team_one_label.grid(row=0, column=0, pady=2.5)

                    team_two_label = ctk.CTkLabel(master=match_frame, text=team_two_text, height=30)
                    team_two_label.grid(row=1, column=0, pady=2.5)

