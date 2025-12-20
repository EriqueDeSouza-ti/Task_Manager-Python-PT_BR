from classes.userdata import User
from classes.user import WinUser
from classes.home import WinHome
from classes.settings import WinConfig
from customtkinter import *
from PIL import Image
from pathlib import Path

set_appearance_mode("dark")
        

class App(CTk):
    def __init__(self, user: User):
        super().__init__()
        self.pos_x = (self.winfo_screenwidth() // 2) - (1200 // 2)
        self.pos_y = (self.winfo_screenheight() // 2) - (800 // 2)
        self.geometry(f"{1200}x{800}+{self.pos_x}+{self.pos_y}")
        self.title("Gerenciador de tarefas")

        self.user = user

        self.dir_icons = Path(__file__).resolve().parents[2]
        self.iconbitmap(self.dir_icons/"img"/"app.ico")

        self.tasks = self.user.tasks
        self.current_win = None
        self.dark_theme  = True

    # ---------------------- UI COMPONENTS ----------------------
        self.top_bar = CTkFrame(self, corner_radius=0, fg_color="#222222")
        self.top_bar.pack(side="top", fill="x")
        self.top_bar.rowconfigure((0, 2), weight=1)
        self.top_bar.columnconfigure((0, 5), weight=1)

        self.user_icon = CTkImage(light_image=Image.open(self.dir_icons/"img"/"user_black.png"),
                                dark_image=Image.open(self.dir_icons/"img"/"user_white.png"),
                                size=(72, 72))
        self.home_icon = CTkImage(light_image=Image.open(self.dir_icons/"img"/"home_black.png"),
                                dark_image=Image.open(self.dir_icons/"img"/"home_white.png"),
                                size=(72, 72))
        self.config_icon = CTkImage(light_image=Image.open(self.dir_icons/"img"/"config_black.png"),
                                dark_image=Image.open(self.dir_icons/"img"/"config_white.png"),
                                size=(72, 72))
        self.logout_icon = CTkImage(light_image=Image.open(self.dir_icons/"img"/"logout_black.png"),
                                dark_image=Image.open(self.dir_icons/"img"/"logout_white.png"),
                                size=(70, 70))
        
        CTkButton(self.top_bar, text="", image=self.user_icon, height=20, width=20,
                corner_radius=0, fg_color="transparent",
                command=lambda: self.slide_to_window(WinUser)).grid(row=1, column=1, padx=1)
        CTkButton(self.top_bar, text="", image=self.home_icon, height=20, width=20,
                corner_radius=0, fg_color="transparent",
                command=lambda: self.slide_to_window(WinHome)).grid(row=1, column=2, padx=1)
        CTkButton(self.top_bar, text="", image=self.config_icon, height=20, width=20,
                corner_radius=0, fg_color="transparent",
                command=lambda: self.slide_to_window(WinConfig)).grid(row=1, column=3, padx=1)
        CTkButton(self.top_bar, text="", image=self.logout_icon, height=20, width=20,
                  corner_radius=0, fg_color="transparent",
                  command=self.logout).grid(row=1, column=4, padx=1)
        
        self.show_win(WinUser)

    # ------------------------ FUNCTIONS ------------------------
    def show_win(self, win_class):
        if self.current_win:
            self.current_win.destroy()
        self.current_win = win_class(self, self.user)
        self.current_win.place(x=0, y=80, relwidth=1, relheight=1)


    def slide_to_window(self, win_class):
        if self.current_win.__class__ == win_class:
            return
        new_window = win_class(self, self.user)
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


    def logout(self):
        win = CTkToplevel(self)
        pos_x = (win.winfo_screenwidth() // 2) - (400 // 2)
        pos_y = (win.winfo_screenheight() // 2) - (200 // 2)
        win.geometry(f"{400}x{200}+{pos_x}+{pos_y}")
        win.resizable(False, False)
        win.title("Sair")
        win.grab_set()
        win.columnconfigure((0, 3), weight=1)

        CTkLabel(win, text="Você quer sair?",
                font=("Arial", 30, "bold")).grid(row=0, column=1, columnspan=2, pady=(30, 60))

        CTkButton(win, text="Sim", command=self.login).grid(row=1, column=1, padx=5)
        CTkButton(win, text="Não", fg_color="#a00000",
                hover_color="#830000", command=win.destroy).grid(row=1, column=2, padx=5)
        
        self.after(200, lambda: win.iconbitmap(self.dir_icons/"img"/"app.ico"))


    def login(self):
        from classes.login import LoginWin
        from lib.file import delete_remember_login

        delete_remember_login()

        self.destroy()
        LoginWin().mainloop()



if __name__ == "__main__":
    App(User(1000, "User", "user@user.com", "user1234")).mainloop()