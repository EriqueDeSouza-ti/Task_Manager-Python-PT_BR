from random import randint
import sys
from pathlib import Path

def check_task_id(list: list):
    if not list:
        return randint(1000, 9999)
    else:
        while True:
            task_id = randint(1000, 9999)
            id = any(t["id"] != task_id for t in list)

            if id:
                return task_id
            
