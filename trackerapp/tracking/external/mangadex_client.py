import requests
from .schemas.anime_schemas import AnimeSchema, AnimeFullSchema, AnimeSearchSchema
from .schemas.episodes_schemas import EpisodeSchema
from .schemas.manga_schemas import MangaSchema, MangaFullSchema, MangaSearchSchema

from typing import List

BASE_URL = "https://api.mangadex.org"

def _get(path, params=None):
    response = requests.get(
        f"{BASE_URL}{path}",
        params=params,
        timeout=10
    )
    response.raise_for_status()

    try:
        return response.json()["data"]
    except (ValueError, KeyError):
        raise RuntimeError("Invalid API response format")
    
def get_manga_feed(id : str) ->MangaSchema:
    data = _get(path=f"/manga/{id}/feed")
    return data

def get_manga(id : str) ->MangaSchema:
    data = _get(path=f"/manga/{id}")
    return data