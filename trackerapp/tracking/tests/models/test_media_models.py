import pytest
from tracking.models.media_models import (
    DemographicModel,
    GenreModel,
    ImagesModel,
    MediaModel,
    ThemeModel,
)


# TESTS GENRE MODEL
#######################################################
def test_genre_model_str(db):
    genre_model = GenreModel.objects.create(name="Action")
    assert str(genre_model) == "Action"


# TESTS DEMOGRAPHIC MODEL
#######################################################
def test_demographic_model_str(db):
    demographic_model = DemographicModel.objects.create(name="Shounen")
    assert str(demographic_model) == "Shounen"


# TESTS THEME MODEL
#######################################################
def test_theme_model_str(db):
    theme_model = ThemeModel.objects.create(name="Mecha")
    assert str(theme_model) == "Mecha"
