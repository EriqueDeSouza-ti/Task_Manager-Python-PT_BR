from customtkinter import *


class WinConfig(CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0)
        self.dark_theme = master.dark_theme


    # ---------------------- UI COMPONENTS ----------------------
        self.main_frame = CTkFrame(self, width=600, height=400)
        self.main_frame.place(rely=0.3, relx=0.5, anchor="center")
        self.main_frame.grid_propagate(False)
        self.main_frame.columnconfigure((0, 3), weight=1)

        CTkLabel(self.main_frame, text="Configurações",
                font=("Arial", 40, "bold")).grid(row=0, column=1, columnspan=2, pady=15)
        CTkLabel(self.main_frame, text="Modo Claro: ",
                font=("Arial", 15)).grid(row=1, column=1)
        self.switch_theme = CTkSwitch(self.main_frame, text="", command=self.change_theme)
        self.switch_theme.grid(row=1, column=2, sticky="w", padx=(0, 50))
    

    # ------------------ CONDITIONAL STRUCTURE ------------------
        if not self.dark_theme:
            self.switch_theme.select()


    # ------------------------ FUNCTIONS ------------------------
    def change_theme(self):
        value = self.switch_theme.get()

        if value == 1:
            set_appearance_mode("light")
            self.master.top_bar.configure(fg_color="#838383")
            self.master.dark_theme = False
        elif value == 0:
            set_appearance_mode("dark")
            self.master.top_bar.configure(fg_color="#222222")
            self.master.dark_theme = True