import pytest

from tracking.external.schemas.anime_schemas import StudioSchema
from tracking.external.schemas.manga_schemas import AuthorSchema
from tracking.external.schemas.media_schemas import (
    DemographicSchema,
    GenreSchema,
    ThemeSchema,
)


@pytest.fixture()
def action_genre_schema():
    return GenreSchema(mal_id=1, name="Action")


@pytest.fixture()
def adventure_genre_schema():
    return GenreSchema(mal_id=2, name="Adventure")


@pytest.fixture()
def fantasy_genre_schema():
    return GenreSchema(mal_id=10, name="Fantasy")


@pytest.fixture()
def martial_arts_theme_schema():
    return ThemeSchema(mal_id=17, name="Martial Arts")


@pytest.fixture()
def school_theme_schema():
    return ThemeSchema(mal_id=23, name="School")


@pytest.fixture()
def team_sports_theme_schema():
    return ThemeSchema(mal_id=78, name="Team Sports")


@pytest.fixture()
def shounen_demographic_schema():
    return DemographicSchema(mal_id=27, name="Shounen")


@pytest.fixture()
def shoujo_demographic_schema():
    return DemographicSchema(mal_id=25, name="Shoujo")


@pytest.fixture()
def madhouse_model(db):
    return StudioSchema(mal_id=11, name="Madhouse")


@pytest.fixture()
def toei_animation_model(db):
    return StudioSchema(mal_id=18, name="Toei Animation")


@pytest.fixture()
def inoue_takehiko_model(db):
    return AuthorSchema(mal_id=1911, name="Inoue, Takehiko")


@pytest.fixture()
def kishimoto_masashi_model(db):
    return AuthorSchema(mal_id=1879, name="Kishimoto, Masashi")
