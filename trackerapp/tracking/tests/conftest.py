from typing import Callable

import pytest

from tracking.models.anime_models import AnimeModel
from tracking.models.manga_models import MangaModel
from tracking.models.media_models import MediaModelStatus

AnimeModelMaker = Callable[[], AnimeModel]
MangaModelMaker = Callable[[], MangaModel]


@pytest.fixture()
def manga_model_example() -> MangaModelMaker:
    def make_manga_model(
        mal_id: int = 0,
        title: str = "Un Manga",
        user_score: int = 6,
        user_completion: MediaModelStatus = MediaModelStatus.IN_PROGRESS,
        user_current_section: int = 10,
        score: float = 4.3,
        synopsis="Exemple de synopsis.",
        number_sections: int = 25,
        rank: int = 78,
        status: str = "Finished",
        number_volumes: int = 25,
    ) -> MangaModel:
        manga_model = MangaModel(
            mal_id=mal_id,
            title=title,
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
            score=score,
            synopsis=synopsis,
            number_sections=number_sections,
            rank=rank,
            status=status,
            number_volumes=number_volumes,
        )
        return manga_model

    return make_manga_model


@pytest.fixture()
def anime_model_example() -> AnimeModelMaker:
    def make_anime_model(
        mal_id: int = 0,
        title: str = "Un Animé",
        user_score: int = 6,
        user_completion: MediaModelStatus = MediaModelStatus.IN_PROGRESS,
        user_current_section: int = 10,
        score: float = 4.3,
        synopsis="Exemple de synopsis.",
        number_sections: int = 25,
        rank: int = 78,
        status: str = "Finished",
        rating: str = "pg13",
        number_episodes: int = 25,
        number_seasons: int = 1,
    ) -> AnimeModel:
        anime_model = AnimeModel(
            mal_id=mal_id,
            title=title,
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
            score=score,
            synopsis=synopsis,
            number_sections=number_sections,
            rank=rank,
            status=status,
            rating=rating,
            number_episodes=number_episodes,
            number_seasons=number_seasons,
        )
        return anime_model

    return make_anime_model


@pytest.fixture()
def one_piece_anime_model() -> AnimeModel:
    return AnimeModel(
        mal_id=17,
        title="One Piece",
        user_score=8,
        user_completion=MediaModelStatus.IN_PROGRESS,
        user_current_section=190,
        score=4.9,
        synopsis="Luffy roi des pirates et tt",
        number_sections=1250,
        rank=2,
        status="airing",
        rating="pg13",
        number_episodes=1250,
        number_seasons=14,
    )


@pytest.fixture()
def hunter_x_hunter_anime_model() -> AnimeModel:
    return AnimeModel(
        mal_id=89,
        title="Hunter x Hunter",
        user_score=8,
        user_completion=MediaModelStatus.IN_PROGRESS,
        user_current_section=190,
        score=4.9,
        synopsis="Go, et son papa Hunter etc.",
        number_sections=148,
        rank=3,
        status="airing",
        rating="r17",
        number_episodes=148,
        number_seasons=6,
    )


@pytest.fixture()
def naruto_manga_model() -> MangaModel:
    return MangaModel(
        mal_id=2,
        title="Naruto",
        user_score=8,
        user_completion=MediaModelStatus.IN_PROGRESS,
        user_current_section=190,
        score=4.9,
        synopsis="Naruto, ninja, Hokage. Démon renard et tout.",
        number_sections=50,
        rank=2,
        status="Finished",
        number_volumes=50,
    )


@pytest.fixture()
def slam_dunk_manga_model() -> MangaModel:
    return MangaModel(
        mal_id=17,
        title="Slam Dunk",
        user_score=8,
        user_completion=MediaModelStatus.COMPLETED,
        user_current_section=20,
        score=4.9,
        synopsis="Sakuragi veut draguer une fille donc il se let au basket.",
        number_sections=20,
        rank=288,
        status="Finished",
        number_volumes=20,
    )
