import customtkinter as ctk

def create_main_rankings(ui):
    root_children = list(ui.root.winfo_children())
    mainpage_children = list(root_children[1].winfo_children())

    for child in mainpage_children:
        child.destroy()

    root_frame = root_children[1]

    # main header
    ranking_header = ctk.CTkLabel(master=root_frame, text=f"World Rankings", width=1720)
    ranking_header.grid(row=0, column=0, sticky="n")

    # ranking region selector

    ranking_region = ctk.CTkFrame(root_frame, width=200)
    ranking_region.grid(row=1, column=0, sticky="w")

    

    # ranking table

    ranking_table = ctk.CTkFrame(root_frame, width=800)
    ranking_table.grid(row=1, column=1)