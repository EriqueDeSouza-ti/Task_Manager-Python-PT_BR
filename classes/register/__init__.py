from customtkinter import *
from lib.utilitys import check_user_id, check_email
from lib.file import save_user, load_users
from classes.userdata import User
from pathlib import Path

set_default_color_theme("dark-blue")


class RegisterWin(CTk):
    def __init__(self):
        super().__init__()
        self.pos_x = (self.winfo_screenwidth() // 2) - (450 // 2)
        self.pos_y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"{450}x{600}+{self.pos_x}+{self.pos_y}")
        self.resizable(False, False)
        self.title("Fazer Registro")

        self.icon = Path(__file__).resolve().parents[2]
        self.iconbitmap(self.icon/"img"/"app.ico")

        self.users = load_users()

        self.main_frame = CTkFrame(self, width=350, corner_radius=0, fg_color="transparent")
        self.main_frame.pack(fill="y", expand=True)

        CTkLabel(self.main_frame, text="Fazer\nregistro.", font=("Arial", 30, "bold")).pack(pady=(10, 30))

        CTkLabel(self.main_frame, text="Nome:", font=("Arial", 20)).pack(anchor="w")
        self.entry_name = CTkEntry(self.main_frame, width=200, height=35)
        self.entry_name.pack(pady=(5, 15))

        CTkLabel(self.main_frame, text="Email:", font=("Arial", 20)).pack(anchor="w")
        self.entry_email = CTkEntry(self.main_frame, width=200, height=35)
        self.entry_email.pack(pady=(5, 15))

        CTkLabel(self.main_frame, text="Senha:", font=("Arial", 20)).pack(anchor="w")
        self.entry_password = CTkEntry(self.main_frame, width=200, height=35, show="*")
        self.entry_password.pack(pady=(5, 15))

        CTkLabel(self.main_frame, text="Confirmar senha:", font=("Arial", 20)).pack(anchor="w")
        self.entry_confirm = CTkEntry(self.main_frame, width=200, height=35, show="*")
        self.entry_confirm.pack(pady=(5, 0))

        self.check_show_pass = CTkCheckBox(self.main_frame, text="Mostrar senha",
                                           command=self.show_password)
        self.check_show_pass.pack(pady=(5, 0))

        self.label_waring = CTkLabel(self.main_frame, text="", text_color="#baee00")
        self.label_waring.pack(pady=(10, 0))

        self.button_register = CTkButton(self.main_frame, text="Registrar", command=self.confirm_register)
        self.button_register.pack(pady=(20, 10))

        self.button_login = CTkButton(self.main_frame, fg_color="transparent",hover=False,
                                    font=("Arial", 12, "underline"),
                                    text="Fazer login",
                                    width=50, height=25,
                                    corner_radius=0,
                                    command=self.login
                                    )
        self.button_login.pack()
        self.button_login.bind("<Enter>", lambda event: self.hovering(True))
        self.button_login.bind("<Leave>", lambda event: self.hovering(False))



    def show_password(self):
        value = self.check_show_pass.get()
        if value == 1:
            self.entry_password.configure(show="")
            self.entry_confirm.configure(show="")
        elif value == 0:
            self.entry_password.configure(show="*")
            self.entry_confirm.configure(show="*")

    
    def confirm_register(self):
        name     = str(self.entry_name.get()).strip()
        email    = str(self.entry_email.get()).strip().lower()
        password = self.entry_password.get()
        confirm  = self.entry_confirm.get()


        if not name or not email or not password or not confirm:
            self.edit_waring("Por favor, preencha os campos.")
            return
        if not "@" in email:
            self.edit_waring("Por favor, escreva um email válido.")
            return
        if len(password) < 8 or " " in password:
            self.edit_waring("A senha deve conter no minímo\n8 caracteres e não deve\nconter espaços.")
            return
        if password != confirm:
            self.edit_waring("As senhas não se encaiaxam!")
            return
        if not self.users:
            id = check_user_id(self.users)
            save_user(User(id, name, email, password), self.users)
            return
        else:
            id = check_user_id(self.users)
            if not check_email(self.users, email):
                from classes.login import LoginWin
                save_user(User(id, name, email, password), self.users)

                self.destroy()
                LoginWin().mainloop()
                return
            else:
                self.edit_waring("Email já cadastrado!")
            


    def hovering(self, value):
        if value:
            self.button_login.configure(text_color="#4934ff")
        else:
            self.button_login.configure(text_color="#ffffff")


    def edit_waring(self, msg: str):
        self.label_waring.configure(text=msg)

        self.after(10000, lambda: self.label_waring.configure(text=""))


    def login(self):
        from classes.login import LoginWin

        self.destroy()
        LoginWin().mainloop()
        





if __name__ == "__main__":
    RegisterWin().mainloop()