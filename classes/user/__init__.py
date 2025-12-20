from customtkinter import *
from classes.userdata import User

class WinUser(CTkFrame):
    def __init__(self, master, user: User):
        super().__init__(master, corner_radius=0)

        self.user = user

        CTkLabel(self, text=f"Bem-vindo, {self.user.name}!",
                font=("Arial", 50, "bold")).place(rely=0.5, relx=0.5, anchor="center")