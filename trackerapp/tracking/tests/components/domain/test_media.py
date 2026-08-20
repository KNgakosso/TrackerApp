from tracking.domain.media import Demographic, Genre, ImagesUrls, Media, Theme
from tracking.enums import MediaCompletion, MediaStatus
from tracking.tests.data.anime_data import HUNTER_X_HUNTER_ANIME, ONE_PIECE_ANIME
from tracking.tests.data.manga_data import NARUTO_MANGA, SLAM_DUNK_MANGA

# TEST IMAGESURLS : FROM_SCHEMA
#######################################################


def test_images_urls_from_schema(mocker):
    images_urls_schema = mocker.Mock()
    images_urls_schema.small_image_url = "http://url_small_image.com"
    images_urls_schema.image_url = "http://url_medium_image.com"
    images_urls_schema.large_image_url = "http://url_large_image.com"

    image_urls = ImagesUrls.from_schema(images_urls_schema)
    assert isinstance(image_urls, ImagesUrls)
    assert image_urls.small_image_url == "http://url_small_image.com"
    assert image_urls.image_url == "http://url_medium_image.com"
    assert image_urls.large_image_url == "http://url_large_image.com"


def test_images_urls_from_schema_none_value(mocker):
    images_urls_schema = mocker.Mock()
    images_urls_schema.small_image_url = None
    images_urls_schema.image_url = None
    images_urls_schema.large_image_url = None

    images_urls = ImagesUrls.from_schema(images_urls_schema)
    assert isinstance(images_urls, ImagesUrls)
    assert images_urls.small_image_url is None
    assert images_urls.image_url is None
    assert images_urls.large_image_url is None


# TESTS GENRE : FROM_SCHEMA
###########################################################


def test_genre_from_schema(mocker):
    genre_schema = mocker.Mock()
    genre_schema.name = "NOM"
    genre = Genre.from_schema(genre_schema)
    assert isinstance(genre, Genre)
    assert genre.name == "NOM"


# TESTS GENRE : FROM_MODEL
###########################################################


def test_genre_from_model(mocker):
    genre_model = mocker.Mock()
    genre_model.name = "NOM"
    genre = Genre.from_model(genre_model)
    assert isinstance(genre, Genre)
    assert genre.name == "NOM"


# TESTS THEME : FROM SCHEMA
###########################################################


def test_theme_from_schema(mocker):
    theme_schema = mocker.Mock()
    theme_schema.name = "NOM"
    theme = Genre.from_schema(theme_schema)
    assert isinstance(theme, Genre)
    assert theme.name == "NOM"


# TESTS THEME : FROM_MODEL
###########################################################


def test_theme_from_model(mocker):
    theme_model = mocker.Mock()
    theme_model.name = "NOM"
    theme = Theme.from_model(theme_model)
    assert isinstance(theme, Theme)
    assert theme.name == "NOM"


# TESTS DEMOGRAPHIC : FROM_SCHEMA
###########################################################


def test_demographic_from_schema(mocker):
    demographic_schema = mocker.Mock()
    demographic_schema.name = "NOM"
    demographic = Demographic.from_schema(demographic_schema)
    assert isinstance(demographic, Demographic)
    assert demographic.name == "NOM"


# TESTS DEMOGRAPHIC : FROM_MODEL
###########################################################


def test_demographic_from_model(mocker):
    demographic_model = mocker.Mock()
    demographic_model.name = "NOM"
    demographic = Demographic.from_model(demographic_model)
    assert isinstance(demographic, Demographic)
    assert demographic.name == "NOM"


# TESTS MEDIA : _BASE_FIELDS_FROM_SCHEMA
###########################################################


def test_base_fields_from_schema_one_piece_anime_schema(mocker, anime_schema_example):
    one_piece_anime_schema = anime_schema_example(**ONE_PIECE_ANIME)
    mocker.patch(
        "tracking.domain.media.ImagesUrls.from_schema",
        side_effect=lambda images_webp: ("from_schema", images_webp),
    )
    mocker.patch(
        "tracking.domain.media.Genre.from_schema",
        side_effect=lambda genre_schema: f"from_schema({genre_schema.name})",
    )
    mocker.patch(
        "tracking.domain.media.Theme.from_schema",
        side_effect=lambda theme_schema: f"from_schema({theme_schema.name})",
    )
    mocker.patch(
        "tracking.domain.media.Demographic.from_schema",
        side_effect=lambda demographic_schema: f"from_schema({demographic_schema.name})",
    )
    data = Media._base_fields_from_schema(one_piece_anime_schema)
    assert data["mal_id"] == 21
    assert data["title"] == "One Piece"
    assert data["title_english"] == "One Piece"
    assert data["title_french"] is None
    assert data["images_urls"] == ("from_schema", one_piece_anime_schema.images.webp)
    assert data["format"] == "TV"
    assert data["synopsis"] == one_piece_anime_schema.synopsis
    assert data["synopsis_translated"] is None
    assert data["score"] == 8.73
    assert data["rank"] == 54
    assert data["themes"] == []
    assert data["genres"] == [
        "from_schema(Action)",
        "from_schema(Adventure)",
        "from_schema(Fantasy)",
    ]
    assert data["demographics"] == ["from_schema(Shounen)"]
    assert data["number_sections"] is None
    assert data["status"] == MediaStatus.CURRENTLY_AIRING
    assert data["user_score"] is None
    assert data["user_completion"] == MediaCompletion.NOT_STARTED
    assert data["user_current_section"] is None
    assert len(data.items()) == 18


def test_base_fields_from_schema_hunter_x_hunter_anime_schema(
    mocker, anime_schema_example
):
    hunter_x_hunter_anime_schema = anime_schema_example(**HUNTER_X_HUNTER_ANIME)
    mocker.patch(
        "tracking.domain.media.ImagesUrls.from_schema",
        side_effect=lambda images_webp: ("from_schema", images_webp),
    )
    mocker.patch(
        "tracking.domain.media.Genre.from_schema",
        side_effect=lambda genre_schema: f"from_schema({genre_schema.name})",
    )
    mocker.patch(
        "tracking.domain.media.Theme.from_schema",
        side_effect=lambda theme_schema: f"from_schema({theme_schema.name})",
    )
    mocker.patch(
        "tracking.domain.media.Demographic.from_schema",
        side_effect=lambda demographic_schema: f"from_schema({demographic_schema.name})",
    )
    data = Media._base_fields_from_schema(hunter_x_hunter_anime_schema)
    assert data["mal_id"] == 11061
    assert data["title"] == "Hunter x Hunter (2011)"
    assert data["title_english"] == "Hunter x Hunter"
    assert data["title_french"] == "Hunter X Hunter"
    assert data["images_urls"] == (
        "from_schema",
        hunter_x_hunter_anime_schema.images.webp,
    )
    assert data["format"] == "TV"
    assert data["synopsis"] == hunter_x_hunter_anime_schema.synopsis
    assert data["synopsis_translated"] is None
    assert data["score"] == 9.03
    assert data["rank"] == 10
    assert data["status"] == MediaStatus.FINISHED_AIRING
    assert data["themes"] == []
    assert data["genres"] == [
        "from_schema(Action)",
        "from_schema(Adventure)",
        "from_schema(Fantasy)",
    ]
    assert data["demographics"] == ["from_schema(Shounen)"]
    assert data["number_sections"] == 148
    assert data["user_score"] is None
    assert data["user_completion"] == MediaCompletion.NOT_STARTED
    assert data["user_current_section"] == 0
    assert len(data.items()) == 18


def test_base_fields_from_schema_naruto_manga_schema(mocker, manga_schema_example):
    naruto_manga_schema = manga_schema_example(**NARUTO_MANGA)
    mocker.patch(
        "tracking.domain.media.ImagesUrls.from_schema",
        side_effect=lambda images_webp: ("from_schema", images_webp),
    )
    mocker.patch(
        "tracking.domain.media.Genre.from_schema",
        side_effect=lambda genre_schema: f"from_schema({genre_schema.name})",
    )
    mocker.patch(
        "tracking.domain.media.Theme.from_schema",
        side_effect=lambda theme_schema: f"from_schema({theme_schema.name})",
    )
    mocker.patch(
        "tracking.domain.media.Demographic.from_schema",
        side_effect=lambda demographic_schema: f"from_schema({demographic_schema.name})",
    )
    data = Media._base_fields_from_schema(naruto_manga_schema)
    assert data["mal_id"] == 11
    assert data["title"] == "Naruto"
    assert data["title_english"] == "Naruto"
    assert data["title_french"] is None
    assert data["images_urls"] == ("from_schema", naruto_manga_schema.images.webp)
    assert data["format"] == "TV"
    assert data["synopsis"] == naruto_manga_schema.synopsis
    assert data["synopsis_translated"] is None
    assert data["score"] == 8.08
    assert data["rank"] == 698
    assert data["themes"] == ["from_schema(Martial Arts)"]
    assert data["genres"] == [
        "from_schema(Action)",
        "from_schema(Adventure)",
        "from_schema(Fantasy)",
    ]
    assert data["demographics"] == ["from_schema(Shounen)"]
    assert data["number_sections"] == 72
    assert data["status"] == MediaStatus.FINISHED
    assert data["user_score"] is None
    assert data["user_completion"] == MediaCompletion.NOT_STARTED
    assert data["user_current_section"] == 0
    assert len(data.items()) == 18


def test_base_fields_from_schema_anime_schema_empty(anime_schema_example):
    anime_schema = anime_schema_example(
        title_english=None,
        titles=[],
        small_image_url=None,
        image_url=None,
        large_image_url=None,
        type_=None,
        synopsis=None,
        score=None,
        rank=None,
        themes=[],
        genres=[],
        status=None,
        demographics=[],
        number_sections=None,
    )

    data = Media._base_fields_from_schema(anime_schema)
    assert data["mal_id"] == 0
    assert data["title"] == "An Anime"
    assert data["title_english"] is None
    assert data["title_french"] is None
    assert data["images_urls"].small_image_url is None
    assert data["images_urls"].image_url is None
    assert data["images_urls"].large_image_url is None
    assert data["format"] is None
    assert data["synopsis"] is None
    assert data["synopsis_translated"] is None
    assert data["score"] is None
    assert data["rank"] is None
    assert data["themes"] == []
    assert data["genres"] == []
    assert data["demographics"] == []
    assert data["number_sections"] is None
    assert data["status"] is None
    assert data["user_score"] is None
    assert data["user_completion"] == MediaCompletion.NOT_STARTED
    assert data["user_current_section"] is None
    assert len(data.items()) == 18


# TESTS MEDIA : _BASE_FIELDS_FROM_MODEL
###########################################################


def test_base_fields_from_model_hunter_x_hunter_anime_model(
    mocker, anime_model_example
):
    hunter_x_hunter_anime_model = anime_model_example(**HUNTER_X_HUNTER_ANIME)
    mocker.patch(
        "tracking.domain.media.Genre.from_model",
        side_effect=lambda genre_model: f"from_model({genre_model.name})",
    )
    mocker.patch(
        "tracking.domain.media.Theme.from_model",
        side_effect=lambda theme_model: f"from_model({theme_model.name})",
    )
    mocker.patch(
        "tracking.domain.media.Demographic.from_model",
        side_effect=lambda demographic_model: f"from_model({demographic_model.name})",
    )
    data = Media._base_fields_from_model(hunter_x_hunter_anime_model)
    assert data["mal_id"] == 11061
    assert data["title"] == "Hunter x Hunter (2011)"
    assert data["title_english"] == "Hunter x Hunter"
    assert data["title_french"] == "Hunter X Hunter"
    assert (
        data["images_urls"].small_image_url
        == hunter_x_hunter_anime_model.small_image_url
    )
    assert data["images_urls"].image_url == hunter_x_hunter_anime_model.image_url
    assert (
        data["images_urls"].large_image_url
        == hunter_x_hunter_anime_model.large_image_url
    )
    assert data["format"] == "TV"
    assert data["synopsis"] == hunter_x_hunter_anime_model.synopsis
    assert (
        data["synopsis_translated"] == hunter_x_hunter_anime_model.synopsis_translated
    )
    assert data["score"] == 9.03
    assert data["rank"] == 10
    assert data["status"] == MediaStatus.FINISHED_AIRING
    assert data["themes"] == []
    assert data["genres"] == [
        "from_model(Action)",
        "from_model(Adventure)",
        "from_model(Fantasy)",
    ]
    assert data["demographics"] == ["from_model(Shounen)"]
    assert data["number_sections"] == 148
    assert data["user_score"] == 10
    assert data["user_completion"] == MediaCompletion.COMPLETED
    assert data["user_current_section"] == 148
    assert len(data.items()) == 18


def test_base_fields_from_model_slam_dunk_manga_model(mocker, manga_model_example):
    slam_dunk_manga_model = manga_model_example(**SLAM_DUNK_MANGA)
    mocker.patch(
        "tracking.domain.media.Genre.from_model",
        side_effect=lambda genre_model: f"from_model({genre_model.name})",
    )
    mocker.patch(
        "tracking.domain.media.Theme.from_model",
        side_effect=lambda theme_model: f"from_model({theme_model.name})",
    )
    mocker.patch(
        "tracking.domain.media.Demographic.from_model",
        side_effect=lambda demographic_model: f"from_model({demographic_model.name})",
    )
    data = Media._base_fields_from_model(slam_dunk_manga_model)
    assert data["mal_id"] == 51
    assert data["title"] == "Slam Dunk"
    assert data["title_english"] == "Slam Dunk"
    assert data["title_french"] is None
    assert data["images_urls"].small_image_url == slam_dunk_manga_model.small_image_url
    assert data["images_urls"].image_url == slam_dunk_manga_model.image_url
    assert data["images_urls"].large_image_url == slam_dunk_manga_model.large_image_url
    assert data["format"] == "Manga"
    assert data["synopsis"] == slam_dunk_manga_model.synopsis
    assert data["synopsis_translated"] == slam_dunk_manga_model.synopsis_translated
    assert data["score"] == 9.09
    assert data["rank"] == 7
    assert data["status"] == MediaStatus.FINISHED
    assert data["themes"] == ["from_model(School)", "from_model(Team Sports)"]
    assert data["genres"] == [
        "from_model(Award Winning)",
        "from_model(Sports)",
    ]
    assert data["demographics"] == ["from_model(Shounen)"]
    assert data["number_sections"] == 31
    assert data["user_score"] is None
    assert data["user_completion"] == MediaCompletion.NOT_STARTED
    assert data["user_current_section"] == 0
    assert len(data.items()) == 18


def test_base_fields_from_model_manga_model_empty(manga_model_example):
    manga_model = manga_model_example(
        title_english="",
        title_french="",
        small_image_url="",
        image_url="",
        large_image_url="",
        format="",
        synopsis="",
        synopsis_translated="",
        score=None,
        rank=None,
        themes=[],
        genres=[],
        status="",
        demographics=[],
        number_sections=None,
        user_score=None,
        user_current_section=None,
    )

    data = Media._base_fields_from_model(manga_model)
    assert data["mal_id"] == 0
    assert data["title"] == "A Manga"
    assert data["title_english"] is None
    assert data["title_french"] is None
    assert data["images_urls"].small_image_url is None
    assert data["images_urls"].image_url is None
    assert data["images_urls"].large_image_url is None
    assert data["format"] is None
    assert data["synopsis"] is None
    assert data["synopsis_translated"] is None
    assert data["score"] is None
    assert data["rank"] is None
    assert data["themes"] == []
    assert data["genres"] == []
    assert data["demographics"] == []
    assert data["number_sections"] is None
    assert data["status"] is None
    assert data["user_score"] is None
    assert data["user_current_section"] is None
    assert len(data.items()) == 18


# TESTS MEDIA : TRANSLATE_SYNOSPSIS
###########################################################


def test_translate_synopsis_language_fr(mocker, anime_example):
    mocker.patch(
        "tracking.domain.media.translate.translate",
        side_effect=lambda q, from_code, to_code: f"Translation of '{q}' from {from_code} to {to_code}",
    )
    anime_domain = anime_example(synopsis_translated=None)
    anime_domain.translate_synopsis("fr")
    assert (
        anime_domain.synopsis_translated == "Translation of 'A synopsis.' from en to fr"
    )


def test_translate_synopsis_language_fr_remplace_translation(mocker, anime_example):
    mocker.patch(
        "tracking.domain.media.translate.translate",
        side_effect=lambda q, from_code, to_code: f"Translation of '{q}' from {from_code} to {to_code}",
    )
    manga_domain = anime_example(synopsis_translated="Previous Translation.")
    manga_domain.translate_synopsis("fr")
    assert (
        manga_domain.synopsis_translated == "Translation of 'A synopsis.' from en to fr"
    )


def test_translate_synopsis_language_fr_none_value(anime_example):

    anime_domain = anime_example(synopsis=None, synopsis_translated=None)
    anime_domain.translate_synopsis("fr")
    assert anime_domain.synopsis_translated is None


def test_translate_synopsis_language_en(anime_example):

    anime_domain = anime_example(synopsis_translated=None)
    anime_domain.translate_synopsis("en")
    assert anime_domain.synopsis_translated == "A synopsis."
    assert anime_domain.synopsis_translated == anime_domain.synopsis


def test_translate_synopsis_language_en_no_remplacement(anime_example):
    anime_domain = anime_example(synopsis_translated="Previous Translation.")
    anime_domain.translate_synopsis("en")
    assert anime_domain.synopsis_translated == "A synopsis."
    assert anime_domain.synopsis_translated == anime_domain.synopsis


def test_translate_synopsis_language_en_none_value(anime_example):
    anime_domain = anime_example(synopsis=None, synopsis_translated=None)
    anime_domain.translate_synopsis("en")
    assert anime_domain.synopsis_translated is None
