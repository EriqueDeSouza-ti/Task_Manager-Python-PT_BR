from pathlib import Path
import json

MAIN_FILE = Path("tasks.json")

def save_file(task_list: list):
    with open(MAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(task_list, f, ensure_ascii=False, indent=2)


def load_file():
    if not MAIN_FILE.exists():
        save_file([])
        return []
    else:
        try:
            with open(MAIN_FILE, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except json.decoder.JSONDecodeError:
            save_file([])
            return []
        else:
            return tasks