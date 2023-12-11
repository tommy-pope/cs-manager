import customtkinter as ctk

from .event_info_page import create_event_info_page


def create_events_page(ui, filter):
    root_children = list(ui.root.winfo_children())
    mainpage_children = list(root_children[1].winfo_children())

    for child in mainpage_children:
        child.destroy()

    root_frame = root_children[1]

    # main header
    events_header = ctk.CTkLabel(
        master=root_frame, text=f"{filter} Events", font=("Arial", 35), width=1720
    )
    events_header.grid(row=0, column=0, columnspan=5, sticky="n", pady=10)

    # Events selector
    events_select = ctk.CTkFrame(root_frame, width=200)
    events_select.grid(row=1, column=0, padx=50)

    upcoming_events = ctk.CTkButton(
        master=events_select,
        text="Upcoming",
        command=lambda: create_events_page(ui, "Upcoming"),
    )
    upcoming_events.grid(row=0, column=0)

    past_events = ctk.CTkButton(
        master=events_select,
        text="Past",
        command=lambda: create_events_page(ui, "Past"),
    )
    past_events.grid(row=1, column=0)

    # events table
    events_table = ctk.CTkFrame(root_frame)
    events_table.grid(row=1, column=1, columnspan=4, sticky="w", pady=25)

    header_row = ctk.CTkFrame(events_table)
    header_row.grid(row=0, column=0, columnspan=3)

    date_header = ctk.CTkLabel(
        header_row, text="Date", width=100, anchor="w", font=("Arial", 25)
    )
    date_header.grid(row=0, column=0)

    name_header = ctk.CTkLabel(
        header_row, text="Name", width=250, anchor="w", font=("Arial", 25)
    )
    name_header.grid(row=0, column=1)

    region_header = ctk.CTkLabel(
        header_row, text="Region", width=125, anchor="w", font=("Arial", 25)
    )
    region_header.grid(row=0, column=2)

    reputation_header = ctk.CTkLabel(
        header_row, text="Reputation", width=125, anchor="w", font=("Arial", 25)
    )
    reputation_header.grid(row=0, column=3)

    events_to_show = ui.db.events if filter == "Upcoming" else ui.db.past_events

    for i, event in enumerate(events_to_show):
        row = ctk.CTkFrame(events_table)
        row.grid(row=i + 1, column=0)

        event_date = (
            f"{event.start_date[0]}/{event.start_date[1]}/{event.start_date[2]}"
        )
        event_name = event.name
        event_region = event.continent
        event_rep = event.rep

        date_widget = ctk.CTkLabel(
            row, text=event_date, width=100, anchor="w", font=("Arial", 15)
        )
        date_widget.grid(row=0, column=0)

        name_widget = ctk.CTkLabel(
            row, text=event_name, width=250, anchor="w", font=("Arial", 15)
        )
        name_widget.grid(row=0, column=1)

        name_widget.bind(
            "<Button-1>", lambda x, copy=event: create_event_info_page(x, ui, copy)
        )

        region_widget = ctk.CTkLabel(
            row, text=event_region, width=125, anchor="w", font=("Arial", 15)
        )
        region_widget.grid(row=0, column=2)

        rep_widget = ctk.CTkLabel(
            row, text=event_rep, width=125, anchor="w", font=("Arial", 15)
        )
        rep_widget.grid(row=0, column=3)
