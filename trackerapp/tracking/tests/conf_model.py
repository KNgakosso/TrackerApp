import pytest

from tracking.models.anime_models import StudioModel
from tracking.models.manga_models import AuthorModel
from tracking.models.media_models import DemographicModel, GenreModel, ThemeModel


@pytest.fixture()
def action_genre_model(db):
    return GenreModel.objects.create(mal_id_anime=1, mal_id_manga=1, name="Action")


@pytest.fixture()
def adventure_genre_model(db):
    return GenreModel.objects.create(mal_id_anime=2, mal_id_manga=2, name="Adventure")


@pytest.fixture()
def fantasy_genre_model(db):
    return GenreModel.objects.create(mal_id_anime=10, mal_id_manga=10, name="Fantasy")


@pytest.fixture()
def martial_arts_theme_model(db):
    return ThemeModel.objects.create(
        mal_id_anime=17, mal_id_manga=17, name="Martial Arts"
    )


@pytest.fixture()
def school_theme_model(db):
    return ThemeModel.objects.create(mal_id_anime=23, mal_id_manga=23, name="School")


@pytest.fixture()
def team_sports_theme_model(db):
    return ThemeModel.objects.create(
        mal_id_anime=77, mal_id_manga=78, name="Team Sports"
    )


@pytest.fixture()
def shounen_demographic_model(db):
    return DemographicModel.objects.create(
        mal_id_anime=27, mal_id_manga=27, name="Shounen"
    )


@pytest.fixture()
def shoujo_demographic_model(db):
    return DemographicModel.objects.create(
        mal_id_anime=25, mal_id_manga=25, name="Shoujo"
    )


@pytest.fixture()
def madhouse_model(db):
    return StudioModel.objects.create(mal_id=11, name="Madhouse")


@pytest.fixture()
def toei_animation_model(db):
    return StudioModel.objects.create(mal_id=18, name="Toei Animation")


@pytest.fixture()
def inoue_takehiko_model(db):
    return AuthorModel.objects.create(mal_id=1911, name="Inoue, Takehiko")


@pytest.fixture()
def kishimoto_masashi_model(db):
    return AuthorModel.objects.create(mal_id=1879, name="Kishimoto, Masashi")
