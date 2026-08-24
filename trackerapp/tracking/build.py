import sqlite3
import time

import requests

DB_URL = "../db.sqlite3"

DEMOGRAPHICS_PARAMS = {
    "filter": "demographics",
    "data": {},
    "table": "tracking_demographicmodel",
}

THEMES_PARAMS = {"filter": "themes", "data": {}, "table": "tracking_thememodel"}

GENRES_PARAMS = {"filter": "genres", "data": {}, "table": "tracking_genremodel"}


def insert(table_name, category_name, category_ids):
    with sqlite3.connect(DB_URL) as db:
        cursor = db.cursor()
        cursor.execute(
            f"INSERT INTO {table_name}(name,mal_id_anime,mal_id_manga) VALUES (?, ?, ?)",
            (category_name, category_ids["mal_id_anime"], category_ids["mal_id_manga"]),
        )
        db.commit()
        cursor.close()


for media_type in ["anime", "manga"]:
    for field_params in [DEMOGRAPHICS_PARAMS, GENRES_PARAMS, THEMES_PARAMS]:
        response = requests.get(
            url=f"https://api.tenrai.org/v1/genres/{media_type}?filter={field_params['filter']}"
        ).json()
        time.sleep(0.35)
        for value in response["data"]:
            field_params["data"].setdefault(
                value["name"], {"mal_id_anime": None, "mal_id_manga": None}
            )[f"mal_id_{media_type}"] = value["mal_id"]

for field_params in [DEMOGRAPHICS_PARAMS, GENRES_PARAMS, THEMES_PARAMS]:
    for category_name, category_ids in field_params["data"].items():
        insert(field_params["table"], category_name, category_ids)
