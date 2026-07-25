from typing import Callable

import pytest

from ...domain.anime import Anime, Studio
from ...domain.enums import AnimeRating, MediaCompletion, MediaStatus
from ...domain.media import Demographic, Genre, ImagesUrls, Theme
from ...external.schemas.anime_schemas import AnimeFullSchema, StudioSchema
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
        title: str = "An Anime",
        small_image_url: str | None = "https:///images/anime/mal_id/small.webp",
        image_url: str | None = "https:///images/anime/mal_id/medium.webp",
        large_image_url: str | None = "https:///images/anime/mal_id/large.webp",
        type_: str | None = "TV",
        synopsis: str | None = "A synopsis.",
        score: float | None = 5.5,
        rank: int | None = 100,
        themes: list[ThemeSchema] = [theme_schema_example()],
        genres: list[GenreSchema] = [genre_schema_example()],
        demographics: list[DemographicSchema] = [demographic_schema_example()],
        number_sections: int | None = 25,
        status: MediaStatus = MediaStatus.FINISHED,
        studios: list[StudioSchema] = [studio_schema_example()],
        duration: str | None = "24 min per ep",
        rating: AnimeRating | None = AnimeRating.G,
        **kwargs
    ) -> AnimeFullSchema:
        return AnimeFullSchema(
            mal_id=mal_id,
            title=title,
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
        small_image_url: str | None = "https:///images/anime/mal_id/small.webp",
        image_url: str | None = "https:///images/anime/mal_id/medium.webp",
        large_image_url: str | None = "https:///images/anime/mal_id/large.webp",
        format: str | None = "TV",
        synopsis: str | None = "A synopsis.",
        score: float | None = 5.5,
        rank: int | None = 100,
        themes: list[Theme] = [theme_example()],
        genres: list[Genre] = [genre_example()],
        demographics: list[Demographic] = [demographic_example()],
        number_sections: int | None = 25,
        status: MediaStatus | None = MediaStatus.FINISHED,
        studios: list[Studio] = [studio_example()],
        duration: str | None = "24 min per ep",
        rating: AnimeRating | None = AnimeRating.G,
        user_score: int | None = 5,
        user_completion: MediaCompletion = MediaCompletion.NOT_STARTED,
        user_current_section: int | None = 0,
    ) -> Anime:
        return Anime(
            mal_id=mal_id,
            title=title,
            images_urls=ImagesUrls(
                small_image_url=small_image_url,
                image_url=image_url,
                large_image_url=large_image_url,
            ),
            format=format,
            synopsis=synopsis,
            number_sections=number_sections,
            score=score,
            rank=rank,
            themes=themes,
            genres=genres,
            demographics=demographics,
            status=status,
            studios=studios,
            duration=duration,
            rating=rating,
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
        )

    return make_anime


@pytest.fixture()
def anime_model_example(db) -> AnimeModelMaker:
    def make_anime_model(
        mal_id: int = 0,
        title: str = "An Anime",
        small_image_url: str | None = "https:///images/anime/mal_id/small.webp",
        image_url: str | None = "https:///images/anime/mal_id/medium.webp",
        large_image_url: str | None = "https:///images/anime/mal_id/large.webp",
        format: str | None = "TV",
        synopsis: str | None = "A synopsis.",
        score: float | None = 5.5,
        rank: int | None = 100,
        themes: list[ThemeModel] = [theme_model_example()],
        genres: list[GenreModel] = [genre_model_example()],
        demographics: list[DemographicModel] = [demographic_model_example()],
        number_sections: int | None = 25,
        status: MediaStatus | None = MediaStatus.FINISHED,
        studios: list[StudioModel] = [studio_model_example()],
        duration: str | None = "24 min per ep",
        rating: AnimeRating | None = AnimeRating.G,
        user_score: int | None = 5,
        user_completion: MediaCompletion = MediaCompletion.NOT_STARTED,
        user_current_section: int | None = 0,
        **kwargs
    ) -> AnimeModel:
        return AnimeModel.objects.create(
            mal_id=mal_id,
            small_image_url=small_image_url,
            image_url=image_url,
            large_image_url=large_image_url,
            format=format,
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
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
        )

    return make_anime_model
