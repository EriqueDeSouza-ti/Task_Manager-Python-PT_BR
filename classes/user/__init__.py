from customtkinter import *

class WinUser(CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0)
        CTkLabel(self, text="Bem-vindo!",
                font=("Arial", 50, "bold")).place(rely=0.5, relx=0.5, anchor="center")