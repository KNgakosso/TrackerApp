from typing import List

import requests

from .exceptions import ExternalApiError
from .schemas.anime_schemas import AnimeFullSchema, AnimeSchema, AnimeSearchSchema
from .schemas.episodes_schemas import EpisodeSchema
from .schemas.manga_schemas import MangaFullSchema, MangaSchema, MangaSearchSchema

BASE_URL = "https://api.tenrai.org/v1"


def _get(path, params=None):
    response = requests.get(f"{BASE_URL}{path}", params=params, timeout=10)
    # response.raise_for_status()

    try:
        return response.json()["data"]
    except requests.RequestException as exc:
        raise ExternalApiError("Tenrai API is unavailable.") from exc
    except (ValueError, KeyError) as exc:
        raise ExternalApiError(
            f"Invalid API response format for path : {path}, params : {params}"
        ) from exc


def get_anime_research_list(params: dict) -> AnimeSearchSchema:
    data = _get(path="/anime", params=params)
    return AnimeSearchSchema(data=data)


def get_manga_research_list(params: dict) -> MangaSearchSchema:
    data = _get(path="/manga", params=params)
    return MangaSearchSchema(data=data)


def get_anime(mal_id: int) -> AnimeSchema:
    data = _get(path=f"/anime/{mal_id}")
    return AnimeSchema(**data)


def get_anime_full(mal_id: int) -> AnimeFullSchema:
    data = _get(path=f"/anime/{mal_id}/full")
    return AnimeFullSchema(**data)


def get_manga(mal_id: int) -> MangaSchema:
    data = _get(path=f"/manga/{mal_id}")
    return MangaFullSchema(**data)


def get_manga_full(mal_id: int) -> MangaFullSchema:
    data = _get(path=f"/manga/{mal_id}/full")
    return MangaFullSchema(**data)


def get_episode(anime_mal_id: int, episode_mal_id: int) -> EpisodeSchema:
    data = _get(path=f"/anime/{anime_mal_id}/episodes/{episode_mal_id}")
    return EpisodeSchema(**data)


def get_episodes_list(anime_mal_id: int) -> List[EpisodeSchema]:
    data = _get(path=f"/anime/{anime_mal_id}/episodes")
    result = [EpisodeSchema(**episode_json) for episode_json in data]
    return result
