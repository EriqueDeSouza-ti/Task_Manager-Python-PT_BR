from lib.file import load_remember_login
from classes.app import App
from classes.login import LoginWin
from pathlib import Path

def main():
    login_file = Path("loginsaved.json")

    if login_file.exists():
        user = load_remember_login()
        App(user).mainloop()
    else:
        LoginWin().mainloop()


if __name__ == "__main__":
    main()