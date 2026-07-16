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
    genre = GenreModel.objects.create(name="Action")
    assert str(genre) == "Action"
