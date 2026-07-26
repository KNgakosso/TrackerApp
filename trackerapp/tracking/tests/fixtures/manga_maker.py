from typing import Callable

import pytest

from ...domain.enums import MediaCompletion, MediaStatus
from ...domain.manga import Author, Manga
from ...domain.media import Demographic, Genre, ImagesUrls, Theme
from ...external.schemas.manga_schemas import MangaFullSchema
from ...external.schemas.media_schemas import ImagesSchema, ImagesUrlsSchema
from ...models.manga_models import MangaModel

MangaModelMaker = Callable[[], MangaModel]
MangaMaker = Callable[[], Manga]
MangaSchemaMaker = Callable[[], MangaFullSchema]


@pytest.fixture()
def manga_schema_example(
    theme_schema_example,
    genre_schema_example,
    demographic_schema_example,
    author_schema_example,
) -> MangaSchemaMaker:
    def make_manga_schema(
        mal_id: int = 0,
        title: str = "An Manga",
        small_image_url: str | None = "https:///images/manga/mal_id/small.webp",
        image_url: str | None = "https:///images/manga/mal_id/medium.webp",
        large_image_url: str | None = "https:///images/manga/mal_id/large.webp",
        type_: str | None = "TV",
        synopsis: str | None = "A synopsis.",
        score: float | None = 5.5,
        rank: int | None = 100,
        themes: list[dict] | None = None,
        genres: list[dict] | None = None,
        demographics: list[dict] | None = None,
        number_sections: int | None = 25,
        status: MediaStatus = MediaStatus.FINISHED,
        chapters: int | None = None,
        authors: list[dict] | None = None,
        **kwargs
    ) -> MangaFullSchema:
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
        authors_schemas = (
            [author_schema_example()]
            if authors is None
            else [author_schema_example(**author_data) for author_data in authors]
        )
        return MangaFullSchema(
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
            chapters=chapters,
            authors=authors_schemas,
        )

    return make_manga_schema


@pytest.fixture()
def manga_example(
    theme_example,
    genre_example,
    demographic_example,
    author_example,
) -> MangaMaker:
    def make_manga(
        mal_id: int = 0,
        title: str = "An Manga",
        small_image_url: str | None = "https:///images/manga/mal_id/small.webp",
        image_url: str | None = "https:///images/manga/mal_id/medium.webp",
        large_image_url: str | None = "https:///images/manga/mal_id/large.webp",
        format: str | None = "TV",
        synopsis: str | None = "A synopsis.",
        score: float | None = 5.5,
        rank: int | None = 100,
        themes: list[Theme] | None = None,
        genres: list[Genre] | None = None,
        demographics: list[Demographic] | None = None,
        number_sections: int | None = 25,
        status: MediaStatus | None = MediaStatus.FINISHED,
        chapters: int | None = None,
        authors: list[Author] | None = None,
        user_score: int | None = 5,
        user_completion: MediaCompletion = MediaCompletion.NOT_STARTED,
        user_current_section: int | None = 0,
    ) -> Manga:
        if themes is None:
            themes = [theme_example()]
        if genres is None:
            genres = [genre_example()]
        if demographics is None:
            demographics = [demographic_example()]
        if authors is None:
            authors = [author_example()]
        return Manga(
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
            authors=authors,
            chapters=chapters,
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
        )

    return make_manga


@pytest.fixture()
def manga_model_example(
    db,
    theme_model_example,
    genre_model_example,
    demographic_model_example,
    author_model_example,
) -> MangaModelMaker:
    def make_manga_model(
        mal_id: int = 0,
        title: str = "An Manga",
        small_image_url: str | None = "https:///images/manga/mal_id/small.webp",
        image_url: str | None = "https:///images/manga/mal_id/medium.webp",
        large_image_url: str | None = "https:///images/manga/mal_id/large.webp",
        format: str | None = "TV",
        synopsis: str | None = "A synopsis.",
        score: float | None = 5.5,
        rank: int | None = 100,
        themes: list[dict] | None = None,
        genres: list[dict] | None = None,
        demographics: list[dict] | None = None,
        number_sections: int | None = 25,
        status: MediaStatus | None = MediaStatus.FINISHED,
        chapters: int | None = None,
        authors: list[dict] | None = None,
        user_score: int | None = 5,
        user_completion: MediaCompletion = MediaCompletion.NOT_STARTED,
        user_current_section: int | None = 0,
        **kwargs
    ) -> MangaModel:
        manga_model = MangaModel.objects.create(
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
            status=status,
            chapters=chapters,
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
        )
        themes_models = (
            [theme_model_example()]
            if themes is None
            else [theme_model_example(**theme_data) for theme_data in themes]
        )
        manga_model.themes.set(themes_models)

        genres_models = (
            [genre_model_example()]
            if genres is None
            else [genre_model_example(**genre_data) for genre_data in genres]
        )
        manga_model.genres.set(genres_models)

        demographics_models = (
            [demographic_model_example()]
            if demographics is None
            else [
                demographic_model_example(**demographic_data)
                for demographic_data in demographics
            ]
        )
        manga_model.demographics.set(demographics_models)

        authors_models = (
            [author_model_example()]
            if authors is None
            else [author_model_example(**author_data) for author_data in authors]
        )
        manga_model.authors.set(authors_models)
        return manga_model

    return make_manga_model
