from typing import Callable

import pytest

from ...domain.anime import Anime, Studio
from ...domain.enums import AnimeRating, MediaCompletion, MediaStatus
from ...domain.media import Demographic, Genre, ImagesUrls, Theme
from ...external.schemas.anime_schemas import AnimeFullSchema
from ...external.schemas.media_schemas import ImagesSchema, ImagesUrlsSchema
from ...models.anime_models import AnimeModel

AnimeModelMaker = Callable[[], AnimeModel]
AnimeMaker = Callable[[], Anime]
AnimeSchemaMaker = Callable[[], AnimeFullSchema]


@pytest.fixture()
def anime_schema_example(
    theme_schema_example,
    genre_schema_example,
    demographic_schema_example,
    studio_schema_example,
) -> AnimeSchemaMaker:
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
        themes: list[dict] | None = None,
        genres: list[dict] | None = None,
        demographics: list[dict] | None = None,
        number_sections: int | None = 25,
        status: MediaStatus = MediaStatus.FINISHED,
        studios: list[dict] | None = None,
        duration: str | None = "24 min per ep",
        rating: AnimeRating | None = AnimeRating.G,
        **kwargs
    ) -> AnimeFullSchema:

        themes_schemas = (
            [theme_schema_example()]
            if themes is None
            else [theme_schema_example(**theme_data) for theme_data in themes]
        )
        genres_schemas = (
            [genre_schema_example()]
            if genres is None
            else [genre_schema_example(**genre_data) for genre_data in genres]
        )

        demographics_schemas = (
            [demographic_schema_example()]
            if demographics is None
            else [
                demographic_schema_example(**demographic_data)
                for demographic_data in demographics
            ]
        )
        studios_schemas = (
            [studio_schema_example()]
            if studios is None
            else [studio_schema_example(**studio_data) for studio_data in studios]
        )
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
            themes=themes_schemas,
            genres=genres_schemas,
            demographics=demographics_schemas,
            status=status,
            studios=studios_schemas,
            duration=duration,
            rating=rating,
        )

    return make_anime_schema


@pytest.fixture()
def anime_example(
    theme_example,
    genre_example,
    demographic_example,
    studio_example,
) -> AnimeMaker:
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
        themes: list[Theme] | None = None,
        genres: list[Genre] | None = None,
        demographics: list[Demographic] | None = None,
        number_sections: int | None = 25,
        status: MediaStatus | None = MediaStatus.FINISHED,
        studios: list[Studio] | None = None,
        duration: str | None = "24 min per ep",
        rating: AnimeRating | None = AnimeRating.G,
        user_score: int | None = 5,
        user_completion: MediaCompletion = MediaCompletion.NOT_STARTED,
        user_current_section: int | None = 0,
    ) -> Anime:
        if themes is None:
            themes = [theme_example()]
        if genres is None:
            genres = [genre_example()]
        if demographics is None:
            demographics = [demographic_example()]
        if studios is None:
            studios = [studio_example()]
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
def anime_model_example(
    db,
    theme_model_example,
    genre_model_example,
    demographic_model_example,
    studio_model_example,
) -> AnimeModelMaker:
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
        themes: list[dict] | None = None,
        genres: list[dict] | None = None,
        demographics: list[dict] | None = None,
        number_sections: int | None = 25,
        status: MediaStatus | None = MediaStatus.FINISHED,
        studios: list[dict] | None = None,
        duration: str | None = "24 min per ep",
        rating: AnimeRating | None = AnimeRating.G,
        user_score: int | None = 5,
        user_completion: MediaCompletion = MediaCompletion.NOT_STARTED,
        user_current_section: int | None = 0,
        **kwargs
    ) -> AnimeModel:
        anime_model = AnimeModel.objects.create(
            mal_id=mal_id,
            title=title,
            small_image_url=small_image_url,
            image_url=image_url,
            large_image_url=large_image_url,
            format=format,
            synopsis=synopsis,
            score=score,
            rank=rank,
            number_sections=number_sections,
            status=status,
            duration=duration,
            rating=rating,
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
        )
        themes_models = (
            [theme_model_example()]
            if themes is None
            else [theme_model_example(**theme_data) for theme_data in themes]
        )
        anime_model.themes.set(themes_models)

        genres_models = (
            [genre_model_example()]
            if genres is None
            else [genre_model_example(**genre_data) for genre_data in genres]
        )
        anime_model.genres.set(genres_models)

        demographics_models = (
            [demographic_model_example()]
            if demographics is None
            else [
                demographic_model_example(**demographic_data)
                for demographic_data in demographics
            ]
        )
        anime_model.demographics.set(demographics_models)

        studios_models = (
            [studio_model_example()]
            if studios is None
            else [studio_model_example(**studio_data) for studio_data in studios]
        )
        anime_model.studios.set(studios_models)

        return anime_model

    return make_anime_model
