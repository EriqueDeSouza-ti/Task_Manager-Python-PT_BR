from classes.userdata import User
from dataclasses import asdict
from typing import List
from pathlib import Path
import json

MAIN_FILE = Path("users.json")
REMEMBER_LOGIN_FILE = Path("loginsaved.json")

        
def check_file():
    with open(MAIN_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)
        return []
    

def save_user_info(user: User):
    users = load_users()
    for i, u in enumerate(users):
        if u["id"] == user.id:
            users[i]["phone"] = user.phone
            users[i]["tasks"] = user.tasks
            break
    with open(MAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def save_user(user: User, users: list):
    user = asdict(user)
    users.append(user)

    with open(MAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def remember_login(user: User):
    user = asdict(user)

    with open(REMEMBER_LOGIN_FILE, "w", encoding="utf-8") as f:
        json.dump(user, f, ensure_ascii=False, indent=2)


def load_remember_login():
    with open(REMEMBER_LOGIN_FILE, "r", encoding="utf-8") as f:
        u = json.load(f)

    return User(u["id"], u["name"],
                u["email"], u["password"], u["phone"], u["tasks"])


def delete_remember_login():
    if REMEMBER_LOGIN_FILE.exists():
        REMEMBER_LOGIN_FILE.unlink()


def load_users():
    if not MAIN_FILE.exists():
        return check_file()
    else:
        try:
            with open(MAIN_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
        except json.decoder.JSONDecodeError:
            return check_file()
        else:
            return users