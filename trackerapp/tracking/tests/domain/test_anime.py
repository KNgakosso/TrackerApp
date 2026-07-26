from tracking.domain.anime import Anime, Studio
from tracking.domain.enums import AnimeRating
from tracking.tests.data.anime_data import HUNTER_X_HUNTER_ANIME, ONE_PIECE_ANIME
from tracking.tests.data.studios_data import MADHOUSE, TOEI_ANIMATION

# TEST STUDIO : FROM_SCHEMA
###########################################################


def test_studio_from_schema_toei_animation(studio_schema_example):
    toei_animation = studio_schema_example(**TOEI_ANIMATION)
    studio = Studio.from_schema(toei_animation)
    assert isinstance(studio, Studio)
    assert studio.name == "Toei Animation"
    assert studio.mal_id == 18


# TEST STUDIO : FROM_MODEL
###########################################################


def test_studio_from_model_madhouse(studio_model_example):
    madhouse = studio_model_example(**MADHOUSE)
    studio = Studio.from_model(madhouse)
    assert isinstance(studio, Studio)
    assert studio.name == "Madhouse"
    assert studio.mal_id == 11


# TESTS ANIME : FROM_SCHEMA
###########################################################


def test_anime_from_schema_one_piece(anime_schema_example):
    one_piece_schema = anime_schema_example(**ONE_PIECE_ANIME)

    anime = Anime.from_schema(one_piece_schema)
    assert isinstance(anime, Anime)
    assert anime.duration == "23 min per ep"
    assert anime.rating == AnimeRating.PG13
    assert len(anime.studios) == 1
    assert isinstance(anime.studios[0], Studio)
    assert anime.studios[0].name == "Toei Animation"


def test_anime_from_schema_empty(anime_schema_example):
    anime_schema_empty = anime_schema_example(duration=None, rating=None, studios=[])
    anime = Anime.from_schema(anime_schema_empty)

    assert isinstance(anime, Anime)
    assert anime.duration is None
    assert anime.rating is None
    assert len(anime.studios) == 0


# TESTS ANIME : FROM_MODEL
###########################################################


def test_anime_from_model_hunter_x_hunter(anime_model_example):
    hunter_x_hunter_model = anime_model_example(**HUNTER_X_HUNTER_ANIME)

    anime = Anime.from_model(hunter_x_hunter_model)
    assert isinstance(anime, Anime)
    assert anime.duration == "23 min per ep"
    assert anime.rating == AnimeRating.PG13
    assert len(anime.studios) == 1
    assert isinstance(anime.studios[0], Studio)
    assert anime.studios[0].name == "Madhouse"


def test_anime_from_model_empty(anime_model_example):
    anime_model_empty = anime_model_example(duration="", rating="", studios=[])

    anime = Anime.from_model(anime_model_empty)
    assert isinstance(anime, Anime)
    assert anime.duration is None
    assert anime.rating is None
    assert len(anime.studios) == 0
