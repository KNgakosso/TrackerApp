from ....domain.anime import Anime
from ....domain.episode import Episode
from ....domain.manga import Manga
from ....domain.media import Media
from ....external.api_client import tenrai_client
from ....forms import SearchForm
from .tenrai_query_builder import build_search_params_anime, build_search_params_manga


def research_media(search_form: SearchForm) -> list[Media]:
    results: list[Media] = []
    if "manga" in search_form.cleaned_data["type"]:
        params = build_search_params_manga(search_form)
        results += [
            Manga.from_schema(manga_schema)
            for manga_schema in tenrai_client.get_manga_research_list(params).data
        ]
    if "anime" in search_form.cleaned_data["type"]:
        params = build_search_params_anime(search_form)
        results += [
            Anime.from_schema(anime_schema)
            for anime_schema in tenrai_client.get_anime_research_list(params).data
        ]
    results = sorted(
        results, key=lambda media: (media.score is None, media.score), reverse=True
    )
    return results


def get_episode(anime_mal_id: int, episode_number: int) -> Episode:
    episode_schema = tenrai_client.get_episode(
        anime_mal_id=anime_mal_id, episode_mal_id=episode_number
    )
    episode = Episode.from_schema(episode_schema)
    return episode


def get_episodes(anime_mal_id: int) -> list[Episode]:
    episode_schema_list = tenrai_client.get_episodes_list(anime_mal_id=anime_mal_id)
    episode_list = [
        Episode.from_schema(episode_schema) for episode_schema in episode_schema_list
    ]
    return episode_list


def get_media(media_mal_id: int, media_type: str) -> Manga | Anime:
    if media_type == "manga":
        return Manga.from_schema(tenrai_client.get_manga(media_mal_id))
    elif media_type == "anime":
        return Anime.from_schema(tenrai_client.get_anime(media_mal_id))
    else:
        raise ValueError(f"Type de média inconnu : {media_type}")


def get_media_full(media_mal_id: int, media_type: str) -> Media:
    if media_type == "manga":
        return Manga.from_schema(tenrai_client.get_manga_full(media_mal_id))
    elif media_type == "anime":
        return Anime.from_schema(tenrai_client.get_anime_full(media_mal_id))
    else:
        raise ValueError(f"Type de média inconnu : {media_type}")
