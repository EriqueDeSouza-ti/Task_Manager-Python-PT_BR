from classes.userdata import User
from typing import List
from random import randint

def check_task_id(list: list):
    if not list:
        return randint(1000, 9999)
    else:
        while True:
            task_id = randint(1000, 9999)
            id = any(t["id"] != task_id for t in list)

            if id:
                return task_id
            


def check_user_id(list: list):
    if not list:
        return randint(1000, 9999)
    else:
        while True:
            user_id = randint(1000, 9999)
            id = any(u["id"] != user_id for u in list)

            if id:
                return user_id


def check_email(list: list, email: str):
    email = any(u["email"] == email for u in list)

    if email:
        return True
    else:
        return False
    
def check_password(list: list, password: str):
    password = any(u["password"] == password for u in list)

    if password:
        return True
    else:
        return False
    

def get_user(list: list, email, password: str):
    user = next((u for u in list
               if u["email"] == email and u["password"] == password), False)

    if user:
        return user
