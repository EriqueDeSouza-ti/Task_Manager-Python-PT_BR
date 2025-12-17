from lib.file import load_file
from classes.user import WinUser
from classes.home import WinHome
from classes.settings import WinConfig
from customtkinter import *
from PIL import Image
from pathlib import Path

set_appearance_mode("dark")
        

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Gerenciador de tarefas")

        self.dir_icons = Path(__file__).resolve().parents[2]
        self.iconbitmap(self.dir_icons/"img"/"app.ico")

        self.tasks = load_file()
        self.current_win = None
        self.dark_theme  = True

    # ---------------------- UI COMPONENTS ----------------------
        self.top_bar = CTkFrame(self, corner_radius=0, fg_color="#222222")
        self.top_bar.pack(side="top", fill="x")
        self.top_bar.rowconfigure((0, 2), weight=1)
        self.top_bar.columnconfigure((0, 4), weight=1)

        self.user_icon = CTkImage(light_image=Image.open(self.dir_icons/"img"/"user_black.png"),
                                dark_image=Image.open(self.dir_icons/"img"/"user_white.png"),
                                size=(72, 72))
        self.home_icon = CTkImage(light_image=Image.open(self.dir_icons/"img"/"home_black.png"),
                                dark_image=Image.open(self.dir_icons/"img"/"home_white.png"),
                                size=(72, 72))
        self.config_icon = CTkImage(light_image=Image.open(self.dir_icons/"img"/"config_black.png"),
                                dark_image=Image.open(self.dir_icons/"img"/"config_white.png"),
                                size=(72, 72))
        
        CTkButton(self.top_bar, text="", image=self.user_icon, height=20, width=20,
                corner_radius=0, fg_color="transparent",
                command=lambda: self.slide_to_window(WinUser)).grid(row=1, column=1, padx=1)
        CTkButton(self.top_bar, text="", image=self.home_icon, height=20, width=20,
                corner_radius=0, fg_color="transparent",
                command=lambda: self.slide_to_window(WinHome)).grid(row=1, column=2, padx=1)
        CTkButton(self.top_bar, text="", image=self.config_icon, height=20, width=20,
                corner_radius=0, fg_color="transparent",
                command=lambda: self.slide_to_window(WinConfig)).grid(row=1, column=3, padx=1)
        
        self.show_win(WinUser)

    # ------------------------ FUNCTIONS ------------------------
    def show_win(self, win_class):
        if self.current_win:
            self.current_win.destroy()
        self.current_win = win_class(self)
        self.current_win.place(x=0, y=80, relwidth=1, relheight=1)


    def slide_to_window(self, win_class):
        if self.current_win.__class__ == win_class:
            return
        new_window = win_class(self)
        width = self.winfo_width()

        new_window.place(x=width, y=80, relwidth=1, relheight=1)

        old_window = self.current_win
        self.current_win = new_window

        self.animate_slide(old_window, new_window, width)


    def animate_slide(self, old_win, new_win, distance, step=40):
        if distance <= 0:
            new_win.place(x=0, y=80, relwidth=1, relheight=1)
            old_win.destroy()
            return
        new_win.place(x=distance, y=80, relwidth=1, relheight=1)
        old_win.place(x=distance - self.winfo_width(),
                      y=80, relwidth=1, relheight=1)
        
        self.after(10, lambda: self.animate_slide(
            old_win, new_win, distance - step
        ))