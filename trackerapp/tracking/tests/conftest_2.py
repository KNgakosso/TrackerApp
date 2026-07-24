from typing import Callable

import pytest

from tracking.external.schemas.anime_schemas import AnimeFullSchema
from tracking.external.schemas.manga_schemas import MangaFullSchema
from tracking.models.anime_models import AnimeModel
from tracking.models.manga_models import MangaModel
from tracking.models.media_models import MediaModelStatus

AnimeModelMaker = Callable[[], AnimeModel]
MangaModelMaker = Callable[[], MangaModel]
AnimeSchemaMaker = Callable[[], AnimeFullSchema]
MangaSchemaMaker = Callable[[], MangaFullSchema]


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
        small_image_url: str = "https:///images/manga/mal_id/small.webp",
        medium_image_url: str = "https:///images/manga/mal_id/medium.webp",
        large_image_url: str = "https:///images/manga/mal_id/large.webp",
        **kwargs
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
            small_image_url=small_image_url,
            medium_image_ur=medium_image_url,
            large_image_ur=large_image_url,
        )
        return manga_model

    return make_manga_model
