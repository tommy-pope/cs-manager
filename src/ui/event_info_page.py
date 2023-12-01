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

