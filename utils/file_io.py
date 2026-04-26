import json
from utils.paths import path_to_bots


def save_bot_json(name_file: str, data: dict):
    with open(path_to_bots(name_file), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_bot_json(name_file: str):
    with open(path_to_bots(name_file), 'r', encoding='utf-8') as f:
        return json.load(f)
