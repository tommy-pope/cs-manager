import customtkinter as ctk

from .team_info_page import create_team_info_page


def create_event_info_page(x, ui, event, filter=None):
    root_children = list(ui.root.winfo_children())
    mainpage_children = list(root_children[1].winfo_children())

    for child in mainpage_children:
        child.destroy()

    root_frame = root_children[1]

    if filter is None:
        filter = "Group" if event.type == "main" and event.round < 2 else "Bracket"

    # main header
    event_header = ctk.CTkLabel(
        master=root_frame, text=f"{event.name}", font=("Arial", 35), width=1720
    )
    event_header.grid(row=0, column=0, columnspan=5, sticky="n", pady=10)

    # event information
    event_info_header = ctk.CTkLabel(
        master=root_frame, text="Event Information:", font=("Arial", 25)
    )
    event_info_header.grid(row=1, column=1, pady=10)

    event_info_box = ctk.CTkFrame(master=root_frame, width=500)
    event_info_box.grid(row=2, column=1)

    event_dates_info = ctk.CTkLabel(
        master=event_info_box,
        text=f"Dates: {event.start_date[0]}/{event.start_date[1]}/{event.start_date[2]} - {event.end_date[0]}/{event.end_date[1]}/{event.end_date[2]}",
        font=("Arial", 15),
    )
    event_dates_info.grid(row=0, column=0, sticky="n")

    event_types_info = ctk.CTkLabel(
        master=event_info_box, text=f"Reputation: {event.rep}", font=("Arial", 15)
    )
    event_types_info.grid(row=1, column=0, sticky="n")

    event_regions_info = ctk.CTkLabel(
        master=event_info_box, text=f"Region: {event.continent}", font=("Arial", 15)
    )
    event_regions_info.grid(row=2, column=0, sticky="n")

    event_num_teams_info = ctk.CTkLabel(
        master=event_info_box,
        text=f"Number of Teams: {len(event.teams)}",
        font=("Arial", 15),
    )
    event_num_teams_info.grid(row=3, column=0, sticky="n")

    # event teams
    event_teams_header = ctk.CTkLabel(
        master=root_frame, text="Teams in Event:", font=("Arial", 25)
    )
    event_teams_header.grid(row=1, column=2, pady=10)

    event_teams_box = ctk.CTkFrame(master=root_frame, width=1000)
    event_teams_box.grid(row=2, column=2)
    event_teams_box.grid_propagate(False)

    for i, team in enumerate(event.teams):
        event_team = ctk.CTkLabel(
            master=event_teams_box,
            text=f"{team.info.name} | {team.info.continent.sname}",
            font=("Arial", 20),
            width=200,
        )
        event_team.grid(row=i // 5, column=i % 5, pady=5)
        event_team.bind(
            "<Button-1>", lambda x, copy=team: create_team_info_page(x, ui, copy)
        )

    event_matches_header_idx = 3
    event_diagram_frame_idx = 4

    # if event with group and bracket
    if event.type == "main" and event.round >= 2:
        event_stage_selector = ctk.CTkFrame(root_frame, 200)
        event_stage_selector.grid(row=3, column=2)

        group_stage = ctk.CTkButton(
            master=event_stage_selector,
            text="Group Stage",
            command=lambda: create_event_info_page(None, ui, event, "Group"),
        )
        group_stage.grid(row=0, column=1)

        bracket_stage = ctk.CTkButton(
            master=event_stage_selector,
            text="Bracket Stage",
            command=lambda: create_event_info_page(None, ui, event, "Bracket"),
        )
        bracket_stage.grid(row=0, column=2)

        event_matches_header_idx = 4
        event_diagram_frame_idx = 5

    event_diagram_text = f"{filter}:"

    # event diagram
    event_matches_header = ctk.CTkLabel(
        master=root_frame, text=event_diagram_text, font=("Arial", 25)
    )

    event_matches_header.grid(
        row=event_matches_header_idx, column=0, pady=10, columnspan=5
    )

    event_diagram_frame = ctk.CTkFrame(master=root_frame, width=1200, height=640)
    event_diagram_frame.grid(
        row=event_diagram_frame_idx, column=0, pady=10, columnspan=5
    )
    event_diagram_frame.grid_propagate(False)

    if filter == "Bracket":
        generate_bracket(event_diagram_frame, ui, event)
    elif filter == "Group":
        generate_group(event_diagram_frame, ui, event)


def generate_bracket(event_diagram_frame, ui, event):
    start_range = 1 if event.type == "qual" else 2

    matches_foreach_round = {
        i: None for i in range(start_range, int(event.total_rounds) + 1)
    }

    # need to determine how many rounds there will be
    for round in range(start_range, int(event.total_rounds) + 1):
        matches_in_round = [
            match for match in event.matches if match.round_in_event == round
        ]
        matches_in_round.extend(
            [match for match in event.results if match.round_in_event == round]
        )

        round_frame = ctk.CTkFrame(master=event_diagram_frame, width=200, height=630)

        if event.type == "main":
            round_frame.grid(row=0, column=round - 2, rowspan=9, pady=5)
        else:
            round_frame.grid(row=0, column=round - 1, rowspan=9, pady=5)

        round_frame.grid_propagate(False)

        # if these games haven't been generated, then fake them
        if len(matches_in_round) == 0:
            # if not an even teams before, special case
            if round == 2:
                fake_matches = int(
                    (len(event.teams) - len(matches_foreach_round[1])) / 2
                )
            else:
                fake_matches = int(len(matches_foreach_round[round - 1]) / 2)

            matches_in_round = [i for i in range(fake_matches)]

        matches_foreach_round[round] = matches_in_round

        if len(matches_in_round) == 1:
            rows_with_matches = [4]
        elif len(matches_in_round) % 2 == 0:
            rows_with_matches = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        else:
            rows_with_matches = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        for i in range(9):
            match_frame = ctk.CTkFrame(master=round_frame, height=70)

            match_frame.grid(column=0, row=i)
            match_frame.grid_propagate(False)

            if i in rows_with_matches:
                match_idx = rows_with_matches.index(i)

                if match_idx > len(matches_in_round) - 1:
                    continue

                team_one_spaces = 0
                team_two_spaces = 0

                if type(matches_in_round[match_idx]) != int:
                    team_one_text = matches_in_round[match_idx].team_one.info.name
                    team_two_text = matches_in_round[match_idx].team_two.info.name

                    team_one_spaces = 20 - len(team_one_text)
                    team_two_spaces = 20 - len(team_two_text)

                    team_one_scores = 0
                    team_two_scores = 0

                    if len(matches_in_round[match_idx].scores) != 0:
                        team_one_scores = ""
                        team_two_scores = ""

                        for score in matches_in_round[match_idx].scores:
                            team_one_scores = f"{team_one_scores}{score[0]}     "
                            team_two_scores = f"{team_two_scores}{score[1]}      "

                    team_one_text = f"{team_one_text}{' '*team_one_spaces}{team_one_scores}"
                    team_two_text = f"{team_two_text}{' '*team_two_spaces}{team_two_scores}"
                else:
                    team_one_text = "TBD"
                    team_two_text = "TBD"

                team_one_label = ctk.CTkLabel(
                    master=match_frame, text=team_one_text, height=30
                )
                team_one_label.grid(row=0, column=0, pady=2.5)

                if team_one_text != "TBD":
                    team_one_label.bind(
                        "<Button-1>",
                        lambda x, copy=matches_in_round[
                            match_idx
                        ].team_one: create_team_info_page(x, ui, copy),
                    )

                team_two_label = ctk.CTkLabel(
                    master=match_frame, text=team_two_text, height=30
                )
                team_two_label.grid(row=1, column=0, pady=2.5)

                if team_two_text != "TBD":
                    team_two_label.bind(
                        "<Button-1>",
                        lambda x, copy=matches_in_round[
                            match_idx
                        ].team_two: create_team_info_page(x, ui, copy),
                    )


def generate_group(event_diagram_frame, ui, event):
    if event.groups is None:
        total_groups = int((len(event.teams) +  len(event.related_events)) / 4)

        groups = [[] for i in range(total_groups)]

        for i in range(len(event.teams)):
            groups[i % 4].append(event.teams[i])
    else:
        groups = event.groups

    for idx, group in enumerate(groups):
        group_header = ctk.CTkLabel(
            master=event_diagram_frame,
            text=f"Group {idx+1}",
            width=300,
            height=50,
        )
        group_header.grid(column=idx, row=0)

        group_frame = ctk.CTkFrame(master=event_diagram_frame, width=300, height=590)
        group_frame.grid(column=idx, row=1)
        group_frame.grid_propagate(False)

        # group header row
        row = ctk.CTkFrame(master=group_frame, width=290, height=50)
        row.grid(column=0, row=0, padx=5)

        position_header = ctk.CTkLabel(master=row, text="Position", width=40)
        position_header.grid(column=0, row=0)

        team_header = ctk.CTkLabel(master=row, text="Team", width=100)
        team_header.grid(column=1, row=0)

        win_header = ctk.CTkLabel(master=row, text="Wins", width=75)
        win_header.grid(column=2, row=0)

        loss_header = ctk.CTkLabel(master=row, text="Losses", width=75)
        loss_header.grid(column=3, row=0)

        for i, team in enumerate(group):
            row = ctk.CTkFrame(master=group_frame, width=290, height=50)
            row.grid(column=0, row=i + 1, padx=5)

            position_header = ctk.CTkLabel(master=row, text=i + 1, width=40)
            position_header.grid(column=0, row=i + 1)

            team_header = ctk.CTkLabel(master=row, text=team.info.name, width=100)
            team_header.grid(column=1, row=i + 1)

            win_header = ctk.CTkLabel(master=row, text=team.wins, width=75)
            win_header.grid(column=2, row=i + 1)

            loss_header = ctk.CTkLabel(master=row, text=team.losses, width=75)
            loss_header.grid(column=3, row=i + 1)
