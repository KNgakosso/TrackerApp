from typing import Callable

import pytest

from ...domain.media import Demographic, Genre, Theme
from ...external.schemas.media_schemas import (
    DemographicSchema,
    GenreSchema,
    ThemeSchema,
)
from ...models.media_models import DemographicModel, GenreModel, ThemeModel

GenreSchemaMaker = Callable[[], GenreSchema]
GenreMaker = Callable[[], Genre]
GenreModelMaker = Callable[[], GenreModel]

ThemeSchemaMaker = Callable[[], ThemeSchema]
ThemeMaker = Callable[[], Theme]
ThemeModelMaker = Callable[[], ThemeModel]

DemographicSchemaMaker = Callable[[], DemographicSchema]
DemographicMaker = Callable[[], Demographic]
DemographicModelMaker = Callable[[], DemographicModel]


# GENRE MAKERS
###############################


@pytest.fixture()
def genre_schema_example() -> GenreSchemaMaker:
    def make_genre_model(
        mal_id: int = 0, name: str = "Un genre", **kwargs
    ) -> GenreSchema:
        if "mal_id_anime" in kwargs.keys():
            mal_id = kwargs["mal_id_anime"]
        return GenreSchema(mal_id=mal_id, name=name)

    return make_genre_model


@pytest.fixture()
def genre_example() -> GenreMaker:
    def make_genre_model(name: str = "Un genre", **kwargs) -> Genre:
        return Genre(name=name)

    return make_genre_model


@pytest.fixture()
def genre_model_example(db) -> GenreModelMaker:
    def make_genre_model(
        mal_id_anime: int = 0, mal_id_manga: int = 0, name: str = "Un genre", **kwargs
    ) -> GenreModel:
        return GenreModel.objects.create(
            mal_id_anime=mal_id_anime, mal_id_manga=mal_id_manga, name=name
        )

    return make_genre_model


# THEME MAKERS
###############################


@pytest.fixture()
def theme_schema_example() -> ThemeSchemaMaker:
    def make_theme_model(
        mal_id: int = 0, name: str = "A Theme", **kwargs
    ) -> ThemeSchema:
        if "mal_id_anime" in kwargs.keys():
            mal_id = kwargs["mal_id_anime"]
        return ThemeSchema(mal_id=mal_id, name=name)

    return make_theme_model


@pytest.fixture()
def theme_example() -> ThemeMaker:
    def make_theme_model(name: str = "A Theme", **kwargs) -> Theme:
        return Theme(name=name)

    return make_theme_model


@pytest.fixture()
def theme_model_example(db) -> ThemeModelMaker:
    def make_theme_model(
        mal_id_anime: int = 0, mal_id_manga: int = 0, name: str = "A Theme", **kwargs
    ) -> ThemeModel:
        return ThemeModel.objects.create(
            mal_id_anime=mal_id_anime, mal_id_manga=mal_id_manga, name=name
        )

    return make_theme_model


# DEMOGRAPHIC MAKERS
###############################


@pytest.fixture()
def demographic_schema_example() -> DemographicSchemaMaker:
    def make_demographic_model(
        mal_id: int = 0, name: str = "A Demographic", **kwargs
    ) -> DemographicSchema:
        if "mal_id_anime" in kwargs.keys():
            mal_id = kwargs["mal_id_anime"]
        return DemographicSchema(mal_id=mal_id, name=name)

    return make_demographic_model


@pytest.fixture()
def demographic_example() -> DemographicMaker:
    def make_demographic_model(name: str = "A Demographic", **kwargs) -> Demographic:
        return Demographic(name=name)

    return make_demographic_model


@pytest.fixture()
def demographic_model_example(db) -> DemographicModelMaker:
    def make_demographic_model(
        mal_id_anime: int = 0,
        mal_id_manga: int = 0,
        name: str = "A Demographic",
        **kwargs
    ) -> DemographicModel:
        return DemographicModel.objects.create(
            mal_id_anime=mal_id_anime, mal_id_manga=mal_id_manga, name=name
        )

    return make_demographic_model
