from typing import Callable

import pytest

from ...domain.anime import Anime, Studio
from ...domain.media import Demographic, Genre, ImagesUrls, MediaStatus, Theme
from ...external.schemas.anime_schemas import AgeRating, AnimeFullSchema, StudioSchema
from ...external.schemas.media_schemas import (
    DemographicSchema,
    GenreSchema,
    ImagesSchema,
    ImagesUrlsSchema,
    ThemeSchema,
)
from ...models.anime_models import AnimeModel, StudioModel
from ...models.media_models import DemographicModel, GenreModel, ThemeModel
from .category_maker import (
    demographic_example,
    demographic_model_example,
    demographic_schema_example,
    genre_example,
    genre_model_example,
    genre_schema_example,
    theme_example,
    theme_model_example,
    theme_schema_example,
)
from .studio_maker import studio_example, studio_model_example, studio_schema_example

AnimeModelMaker = Callable[[], AnimeModel]
AnimeMaker = Callable[[], Anime]
AnimeSchemaMaker = Callable[[], AnimeFullSchema]


@pytest.fixture()
def anime_schema_example() -> AnimeSchemaMaker:
    def make_anime_schema(
        mal_id: int = 0,
        type_: str = "TV",
        title: str = "An Anime",
        small_image_url: str = "https:///images/anime/mal_id/small.webp",
        image_url: str = "https:///images/anime/mal_id/medium.webp",
        large_image_url: str = "https:///images/anime/mal_id/large.webp",
        synopsis: str = "A synopsis.",
        score: float = 4.3,
        number_sections: int = 25,
        rank: int = 78,
        themes: list[ThemeSchema] = [theme_schema_example()],
        genres: list[GenreSchema] = [genre_schema_example()],
        demographics: list[DemographicSchema] = [demographic_schema_example()],
        status: str = "Finished",
        studios: list[StudioSchema] = [studio_schema_example()],
        duration: str = "24 min per ep",
        rating: AgeRating = AgeRating.G,
        **kwargs
    ) -> AnimeFullSchema:
        return AnimeFullSchema(
            mal_id=mal_id,
            images=ImagesSchema(
                webp=ImagesUrlsSchema(
                    small_image_url=small_image_url,
                    image_url=image_url,
                    large_image_url=large_image_url,
                ),
                jpg=ImagesUrlsSchema(
                    small_image_url=None, image_url=None, large_image_url=None
                ),
            ),
            type=type_,
            title=title,
            score=score,
            synopsis=synopsis,
            number_sections=number_sections,
            rank=rank,
            themes=themes,
            genres=genres,
            demographics=demographics,
            status=status,
            studios=studios,
            duration=duration,
            rating=rating,
        )

    return make_anime_schema


@pytest.fixture()
def anime_example() -> AnimeMaker:
    def make_anime(
        mal_id: int = 0,
        title: str = "An Anime",
        small_image_url: str = "https:///images/anime/mal_id/small.webp",
        image_url: str = "https:///images/anime/mal_id/medium.webp",
        large_image_url: str = "https:///images/anime/mal_id/large.webp",
        synopsis: str = "A synopsis.",
        score: float = 4.3,
        number_sections: int = 25,
        rank: int = 78,
        themes: list[Theme] = [theme_example()],
        genres: list[Genre] = [genre_example()],
        demographics: list[Demographic] = [demographic_example()],
        status: str = "Finished",
        user_score: int = 5,
        user_completion: MediaStatus = MediaStatus.NOT_STARTED,
        user_current_section: int = 0,
        studios: list[Studio] = [studio_example()],
        duration: str = "24 min per ep",
        rating: AgeRating = AgeRating.G,
    ) -> Anime:
        return Anime(
            mal_id=mal_id,
            images_urls=ImagesUrls(
                small_image_url=small_image_url,
                medium_image_url=image_url,
                large_image_url=large_image_url,
            ),
            title=title,
            score=score,
            synopsis=synopsis,
            number_sections=number_sections,
            rank=rank,
            themes=themes,
            genres=genres,
            demographics=demographics,
            status=status,
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
            studios=studios,
            duration=duration,
            rating=rating,
        )

    return make_anime


@pytest.fixture()
def anime_model_example() -> AnimeModelMaker:
    def make_anime_model(
        mal_id: int = 0,
        title: str = "An Anime",
        small_image_url: str = "https:///images/anime/mal_id/small.webp",
        image_url: str = "https:///images/anime/mal_id/medium.webp",
        large_image_url: str = "https:///images/anime/mal_id/large.webp",
        synopsis: str = "A synopsis.",
        score: float = 4.3,
        number_sections: int = 25,
        rank: int = 78,
        themes: list[ThemeModel] = [theme_model_example()],
        genres: list[GenreModel] = [genre_model_example()],
        demographics: list[DemographicModel] = [demographic_model_example()],
        status: str = "Finished",
        studios: list[StudioModel] = [studio_model_example()],
        duration: str = "24 min per ep",
        rating: AgeRating = AgeRating.G,
        **kwargs
    ) -> AnimeModel:
        return AnimeModel(
            mal_id=mal_id,
            small_image_url=small_image_url,
            image_url=image_url,
            large_image_url=large_image_url,
            title=title,
            score=score,
            synopsis=synopsis,
            number_sections=number_sections,
            rank=rank,
            themes=themes,
            genres=genres,
            demographics=demographics,
            status=status,
            studios=studios,
            duration=duration,
            rating=rating,
        )

    return make_anime_model
