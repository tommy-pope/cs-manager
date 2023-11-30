import customtkinter as ctk

def create_event_info_page(x, ui, event):
    root_children = list(ui.root.winfo_children())
    mainpage_children = list(root_children[1].winfo_children())

    for child in mainpage_children:
        child.destroy()

    root_frame = root_children[1]

    print(event.name)
