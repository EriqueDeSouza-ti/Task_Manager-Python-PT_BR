from customtkinter import *
from lib.file import load_users, remember_login
from lib.utilitys import check_email, check_password, get_user
from classes.userdata import User
from pathlib import Path



class LoginWin(CTk):
    def __init__(self):
        super().__init__()
        self.pos_x = (self.winfo_screenwidth() // 2) - (350 // 2)
        self.pos_y = (self.winfo_screenheight() // 2) - (480 // 2)
        self.geometry(f"{350}x{480}+{self.pos_x}+{self.pos_y}")
        self.resizable(False, False)
        self.title("Fazer Login")
        
        self.icons = Path(__file__).resolve().parents[2]
        self.iconbitmap(self.icons/"img"/"app.ico")

        self.users = load_users()

        self.main_frame = CTkFrame(self, width=350, corner_radius=0, fg_color="transparent")
        self.main_frame.pack(fill="y", expand=True)

        CTkLabel(self.main_frame, text="Fazer login", font=("Arial", 30, "bold")).pack(pady=(10, 30))

        CTkLabel(self.main_frame, text="Email:", font=("Arial", 20)).pack(anchor="w")
        self.entry_email = CTkEntry(self.main_frame, width=200, height=35)
        self.entry_email.pack(pady=(5, 15))

        CTkLabel(self.main_frame, text="Senha:", font=("Arial", 20)).pack(anchor="w")
        self.entry_password = CTkEntry(self.main_frame, width=200, height=35, show="*")
        self.entry_password.pack(pady=5)
        
        self.check_show = CTkCheckBox(self.main_frame, text="Mostrar senha",
                                    command=self.show_password)
        self.check_show.pack(anchor="w")

        self.button_forgot = CTkButton(self.main_frame, font=("Arial", 12, "underline"),
                height=20, width=100, hover=False, fg_color="transparent",
                text="Esqueci minha senha.", corner_radius=0,
                command=lambda: print("Forgot my password"))
        self.button_forgot.pack(anchor="center", pady=(10, 0))
        self.button_forgot.bind("<Enter>", lambda event: self.hovering(self.button_forgot, True))
        self.button_forgot.bind("<Leave>", lambda event: self.hovering(self.button_forgot, False))

        self.label_waring = CTkLabel(self.main_frame, text="", text_color="#baee00")
        self.label_waring.pack(pady=10)

        self.check_remember = CTkCheckBox(self.main_frame, text="Lembrar login")
        self.check_remember.pack(pady=10)

        CTkButton(self.main_frame, text="Fazer Login", command=self.login).pack(pady=10)
        self.button_register = CTkButton(self.main_frame, text="Fazer registro.",
                  width=80, height=20, corner_radius=0, font=("Arial", 12, "underline"),
                  fg_color="transparent", hover=False, command=self.register)
        self.button_register.pack()
        self.button_register.bind("<Enter>", lambda event: self.hovering(self.button_register, True))
        self.button_register.bind("<Leave>", lambda event: self.hovering(self.button_register, False))


    def show_password(self):
        value = self.check_show.get()

        if value == 1:
            self.entry_password.configure(show="")
        else:
            self.entry_password.configure(show="*")


    def login(self):
        email    = self.entry_email.get()
        password = self.entry_password.get()

        if not email or not password:
            self.edit_waring("Por favor, preencha os campos!")
            return

        if check_email(self.users, email) and check_password(self.users, password):
            u = get_user(self.users, email, password)

            if self.check_remember.get() == 1:
                remember_login(User(u["id"], u["name"], u["email"],
                        u["password"], u["phone"], u["tasks"]))
            from classes.app import App

            self.destroy()
            App(User(u["id"], u["name"], u["email"],
                    u["password"], u["phone"], u["tasks"])).mainloop()
        else:
            self.edit_waring("Email ou senha incorretos!")
            

    def register(self):
        from classes.register import RegisterWin

        self.destroy()
        RegisterWin().mainloop()


    def hovering(self, target, value):
        if value:
            target.configure(text_color="#4934ff")
        else:
            target.configure(text_color="#ffffff")


    def edit_waring(self, msg: str):
        self.label_waring.configure(text=msg)

        self.after(10000, lambda: self.label_waring.configure(text=""))








if __name__ == "__main__":
    LoginWin().mainloop()