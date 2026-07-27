from typing import List

import requests

from .schemas.anime_schemas import AnimeFullSchema, AnimeSchema, AnimeSearchSchema
from .schemas.episodes_schemas import EpisodeSchema
from .schemas.manga_schemas import MangaFullSchema, MangaSchema, MangaSearchSchema

BASE_URL = "https://api.mangadex.org"


def _get(path: str, params: dict | None = None):
    response = requests.get(f"{BASE_URL}{path}", params=params, timeout=10)
    response.raise_for_status()

    try:
        return response.json()["data"]
    except (ValueError, KeyError):
        raise RuntimeError("Invalid API response format")


def get_manga_feed(id: str) -> MangaSchema:
    data = _get(path=f"/manga/{id}/feed")
    return data


def get_manga(id: str) -> MangaSchema:
    data = _get(path=f"/manga/{id}")
    return data
