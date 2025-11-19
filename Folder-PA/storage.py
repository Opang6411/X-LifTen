import json
import os

BASE_DIR = os.path.dirname(__file__)
ANIME_PATH = os.path.join(BASE_DIR, 'data-anime.json')
AKUN_PATH = os.path.join(BASE_DIR, 'data-akun.json')


def _load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# data dimuat sekali saat modul diimport
data_anime = _load_json(ANIME_PATH)
akun = _load_json(AKUN_PATH)


def save_anime():
    with open(ANIME_PATH, 'w', encoding='utf-8') as f:
        json.dump(data_anime, f, indent=4, ensure_ascii=False)


def save_akun():
    with open(AKUN_PATH, 'w', encoding='utf-8') as f:
        json.dump(akun, f, indent=4, ensure_ascii=False)
