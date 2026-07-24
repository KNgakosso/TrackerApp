from typing import Callable

import pytest

from ...domain.manga import Author, Manga
from ...domain.media import Demographic, Genre, ImagesUrls, MediaStatus, Theme
from ...external.schemas.manga_schemas import AuthorSchema, MangaFullSchema
from ...external.schemas.media_schemas import (
    DemographicSchema,
    GenreSchema,
    ImagesSchema,
    ImagesUrlsSchema,
    ThemeSchema,
)
from ...models.manga_models import AuthorModel, MangaModel
from ...models.media_models import DemographicModel, GenreModel, ThemeModel
from .author_maker import author_example, author_model_example, author_schema_example
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

MangaModelMaker = Callable[[], MangaModel]
MangaMaker = Callable[[], Manga]
MangaSchemaMaker = Callable[[], MangaFullSchema]


@pytest.fixture()
def manga_schema_example() -> MangaSchemaMaker:
    def make_manga_schema(
        mal_id: int = 0,
        type_: str = "TV",
        title: str = "An Manga",
        small_image_url: str = "https:///images/manga/mal_id/small.webp",
        image_url: str = "https:///images/manga/mal_id/medium.webp",
        large_image_url: str = "https:///images/manga/mal_id/large.webp",
        synopsis: str = "A synopsis.",
        score: float = 4.3,
        number_sections: int = 25,
        rank: int = 78,
        themes: list[ThemeSchema] = [theme_schema_example()],
        genres: list[GenreSchema] = [genre_schema_example()],
        demographics: list[DemographicSchema] = [demographic_schema_example()],
        status: str = "Finished",
        authors: list[AuthorSchema] = [author_schema_example()],
        chapters: int = 300,
        **kwargs
    ) -> MangaFullSchema:
        return MangaFullSchema(
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
            chapters=chapters,
            authors=authors,
        )

    return make_manga_schema


@pytest.fixture()
def manga_example() -> MangaMaker:
    def make_manga(
        mal_id: int = 0,
        title: str = "An Manga",
        small_image_url: str = "https:///images/manga/mal_id/small.webp",
        image_url: str = "https:///images/manga/mal_id/medium.webp",
        large_image_url: str = "https:///images/manga/mal_id/large.webp",
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
        authors: list[Author] = [author_example()],
        number_chapters: int = 300,
    ) -> Manga:
        return Manga(
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
            authors=authors,
            number_chapters=number_chapters,
        )

    return make_manga


@pytest.fixture()
def manga_model_example() -> MangaModelMaker:
    def make_manga_model(
        mal_id: int = 0,
        title: str = "An Manga",
        small_image_url: str = "https:///images/manga/mal_id/small.webp",
        image_url: str = "https:///images/manga/mal_id/medium.webp",
        large_image_url: str = "https:///images/manga/mal_id/large.webp",
        synopsis: str = "A synopsis.",
        score: float = 4.3,
        number_sections: int = 25,
        rank: int = 78,
        themes: list[ThemeModel] = [theme_model_example()],
        genres: list[GenreModel] = [genre_model_example()],
        demographics: list[DemographicModel] = [demographic_model_example()],
        user_score: int = 5,
        user_completion: MediaStatus = MediaStatus.NOT_STARTED,
        user_current_section: int = 0,
        status: str = "Finished",
        authors: list[AuthorModel] = [author_model_example()],
        **kwargs
    ) -> MangaModel:
        return MangaModel(
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
            authors=authors,
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
        )

    return make_manga_model
