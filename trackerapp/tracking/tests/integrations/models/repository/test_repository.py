import pytest
from tracking.enums import MediaCompletion
from tracking.models.anime_models import AnimeModel
from tracking.models.manga_models import MangaModel
from tracking.models.media_models import DemographicModel, GenreModel, ThemeModel
from tracking.models.repository import repository
from tracking.tests.data.anime_data import (
    GREAT_PRETENDER_ANIME,
    KISEIJUU_ANIME,
    ONE_PIECE_ANIME,
)
from tracking.tests.data.categories_data import (
    ACTION_GENRE,
    SHOUNEN_DEMOGRAPHIC,
    TEAM_SPORTS_THEME,
)
from tracking.tests.data.manga_data import (
    CHAINSAW_MAN_MANGA,
    SLAM_DUNK_MANGA,
    VAGABOND_MANGA,
)

# TESTS _GET_GENRE_MODEL
##############################################


def test_get_genre_model(genre_model_example):
    action_genre = genre_model_example(**ACTION_GENRE)
    genre_model = repository.get_genre_model(name="Action")

    assert isinstance(genre_model, GenreModel)
    assert genre_model.name == "Action"
    assert genre_model.mal_id_anime == 1
    assert genre_model.mal_id_manga == 1


def test_get_genre_model_none_mal_ids(genre_model_example):
    new_genre = genre_model_example(
        name="Genre Sans mal_id", mal_id_anime=None, mal_id_manga=None
    )
    genre_model = repository.get_genre_model(name="Genre Sans mal_id")
    assert isinstance(genre_model, GenreModel)
    assert genre_model.name == "Genre Sans mal_id"
    assert genre_model.mal_id_anime is None
    assert genre_model.mal_id_manga is None


def test_get_genre_model_value_error(db):
    with pytest.raises(ValueError) as e:
        repository.get_genre_model(name="Genre Inexistant")
    assert str(e.value) == "Aucun genre trouvé au nom de Genre Inexistant."


# TESTS _GET_THEME_MODEL
##############################################


def test_get_theme_model(theme_model_example):
    team_sports_theme = theme_model_example(**TEAM_SPORTS_THEME)
    theme_model = repository.get_theme_model(name="Team Sports")

    assert isinstance(theme_model, ThemeModel)
    assert theme_model.name == "Team Sports"
    assert theme_model.mal_id_anime == 78
    assert theme_model.mal_id_manga == 77


def test_get_theme_model_none_mal_ids(theme_model_example):
    new_theme = theme_model_example(
        name="Thème Sans mal_id", mal_id_anime=None, mal_id_manga=None
    )
    theme_model = repository.get_theme_model(name="Thème Sans mal_id")
    assert isinstance(theme_model, ThemeModel)
    assert theme_model.name == "Thème Sans mal_id"
    assert theme_model.mal_id_anime is None
    assert theme_model.mal_id_manga is None


def test_get_theme_model_value_error(db):
    with pytest.raises(ValueError) as e:
        repository.get_theme_model(name="Thème Inexistant")
    assert str(e.value) == "Aucun thème trouvé au nom de Thème Inexistant."


# TESTS _GET_DEMOGRAPHIC_MODEL
##############################################


def test_get_demographic_model(demographic_model_example):
    shounen_demographic = demographic_model_example(**SHOUNEN_DEMOGRAPHIC)
    demographic_model = repository.get_demographic_model(name="Shounen")

    assert isinstance(demographic_model, DemographicModel)
    assert demographic_model.name == "Shounen"
    assert demographic_model.mal_id_anime == 27
    assert demographic_model.mal_id_manga == 27


def test_get_demographic_model_none_mal_ids(demographic_model_example):
    new_demographic = demographic_model_example(
        name="Démographie Sans mal_id", mal_id_anime=None, mal_id_manga=None
    )
    demographic_model = repository.get_demographic_model(name="Démographie Sans mal_id")
    assert isinstance(demographic_model, DemographicModel)
    assert demographic_model.name == "Démographie Sans mal_id"
    assert demographic_model.mal_id_anime is None
    assert demographic_model.mal_id_manga is None


def test_get_demographic_model_value_error(db):
    with pytest.raises(ValueError) as e:
        repository.get_demographic_model(name="Démographie Inexistante")
    assert (
        str(e.value) == "Aucune démographie trouvée au nom de Démographie Inexistante."
    )


# TESTS _GET_MEDIA_MODEL
##############################################


def test_get_media_model_anime(db_example):
    anime_model = repository.get_media_model(mal_id=21, media_type="anime")
    assert isinstance(anime_model, AnimeModel)
    assert anime_model.title == "One Piece"


def test_get_media_model_manga(db_example):
    manga_model = repository.get_media_model(mal_id=51, media_type="manga")
    assert isinstance(manga_model, MangaModel)
    assert manga_model.title == "Slam Dunk"


@pytest.mark.parametrize("media_type", ["manga", "anime"])
def test_get_media_model_value_error(db, media_type):
    with pytest.raises(ValueError) as e:
        repository.get_media_model(mal_id=1, media_type=media_type)
    assert str(e.value) == f"Aucun {media_type} trouvé pour l'id 1."


# TESTS _GET_MEDIA_MODELS
##############################################


def test_get_media_models_no_filters(db_example):
    medias_models = repository.get_medias_models()
    assert len(medias_models) == 4
    titles = set()
    for media_model in medias_models:
        titles.add(media_model.title)
    assert titles == {"One Piece", "Hunter x Hunter (2011)", "Slam Dunk", "Naruto"}


def test_get_media_models_filters(db_example):
    ###############
    # À COMPLÉTER #
    ###############
    pass


def test_get_medias_models_value_error_invalid_filters(db_example):
    with pytest.raises(ValueError) as e:
        medias_models = repository.get_medias_models(invalid_field="value")
    assert str(e.value).startswith("Filtres de recherche invalides : ")


# TESTS _SET_MEDIA_MODEL_USER_COMPLETION
##############################################


@pytest.mark.parametrize(
    "completion",
    [
        MediaCompletion.COMPLETED,
        MediaCompletion.IN_PROGRESS,
        MediaCompletion.NOT_STARTED,
    ],
)
def test_set_user_completion_anime(anime_model_example, completion):
    kiseijuu_anime_model = anime_model_example(**KISEIJUU_ANIME)
    result = repository.set_media_model_user_completion(
        kiseijuu_anime_model, completion
    )
    assert result == completion
    assert kiseijuu_anime_model.user_completion == completion


@pytest.mark.parametrize(
    "completion",
    [
        MediaCompletion.COMPLETED,
        MediaCompletion.IN_PROGRESS,
        MediaCompletion.NOT_STARTED,
    ],
)
def test_set_user_completion_manga(manga_model_example, completion):
    chainsaw_man_manga_model = manga_model_example(**CHAINSAW_MAN_MANGA)
    result = repository.set_media_model_user_completion(
        chainsaw_man_manga_model, completion
    )
    assert result == completion
    assert chainsaw_man_manga_model.user_completion == completion


# TESTS _SET_MEDIA_MODEL_USER_SCORE
##############################################


@pytest.mark.parametrize("score", [None, 0, 10])
def test_set_user_score_anime(anime_model_example, score):
    one_piece_anime_model = anime_model_example(**ONE_PIECE_ANIME)
    result = repository.set_media_model_user_score(one_piece_anime_model, score)
    assert result == score
    assert one_piece_anime_model.user_score == score


@pytest.mark.parametrize("score", [None, 0, 10])
def test_set_user_score_manga(manga_model_example, score):
    slam_dunk_manga_model = manga_model_example(**SLAM_DUNK_MANGA)
    result = repository.set_media_model_user_score(slam_dunk_manga_model, score)
    assert result == score
    assert slam_dunk_manga_model.user_score == score


@pytest.mark.parametrize("score", [-17, -1, 11, 488])
def test_set_user_score_manga_invalid(manga_model_example, score):
    slam_dunk_manga_model = manga_model_example(**SLAM_DUNK_MANGA)
    with pytest.raises(ValueError) as e:
        repository.set_media_model_user_score(slam_dunk_manga_model, score)
    assert (
        str(e.value) == "Le Score doit être un entier entre 0 et 10, ou la valeur None."
    )


# TESTS _SET_MEDIA_MODEL_USER_CURRENT_SECTION
##############################################


@pytest.mark.parametrize("current_section", [None, 0, 1, 20])
def test_set_user_current_section_anime(anime_model_example, current_section):
    great_pretender_anime_model = anime_model_example(**GREAT_PRETENDER_ANIME)
    result = repository.set_media_model_user_current_section(
        great_pretender_anime_model, current_section
    )
    assert result == current_section
    assert great_pretender_anime_model.user_current_section == current_section


@pytest.mark.parametrize("current_section", [None, 0, 1, 20])
def test_set_user_current_section_manga(manga_model_example, current_section):
    vagabond_manga_model = manga_model_example(**VAGABOND_MANGA)
    result = repository.set_media_model_user_current_section(
        vagabond_manga_model, current_section
    )
    assert result == current_section
    assert vagabond_manga_model.user_current_section == current_section
