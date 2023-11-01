import customtkinter as ctk


class UI:
    def __init__(self, db) -> None:
        self.root = None
        self.db = db

    def create_application(self) -> ctk.CTk:
        ctk.set_appearance_mode("dark")

        app = ctk.CTk()
        app.geometry("1920x1080")
        self.root=app

        self.create_sidenavbar()
 
    def create_sidenavbar(self):
        frame = ctk.CTkFrame(self.root, bg_color="gray",width=600, height=1080)
        frame.grid(row=0, column=0)

        date_label = ctk.CTkLabel(master=frame, text=f"{self.db.date[0]}/{self.db.date[1]}/{self.db.date[2]}")
        date_label.grid(row=0, column=0, pady=10, padx=10)
    
        advance_button = ctk.CTkButton(master=frame, text="Advance", command=lambda: self.db.advance(self))
        advance_button.grid(row=1, column=0, pady=10, padx=10)

        ranking_button = ctk.CTkButton(master=frame, text="Rankings")
        ranking_button.grid(row=2, column=0, pady=10, padx=10)

        events_button = ctk.CTkButton(master=frame, text="Events")
        events_button.grid(row=3, column=0, pady=10, padx=10)

    def update_date(self):
        root_children = list(self.root.children.values())
        sidenav_children = list(root_children[0].children.values())
        date_label = sidenav_children[1]
        
        date_label.configure(text=f"{self.db.date[0]}/{self.db.date[1]}/{self.db.date[2]}")
