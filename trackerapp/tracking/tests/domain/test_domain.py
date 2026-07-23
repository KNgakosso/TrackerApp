from unittest.mock import patch

from tracking.domain.media import (
    Demographic,
    Genre,
    ImagesUrls,
    Media,
    MediaStatus,
    Theme,
)
from tracking.domain.watchlist import Watchlist
from tracking.models.watchlist_model import WatchlistModel

# TEST WATCHLIST
#######################################################


def test_watchlist_from_model_no_medias(mocker):
    mock_watchlist_model = mocker.Mock()
    mock_watchlist_model.name = "Liste"
    mock_watchlist_model.medias.all = lambda: []

    watchlist = Watchlist.from_model(mock_watchlist_model)

    assert isinstance(watchlist, Watchlist)
    assert watchlist.name == "Liste"
    assert watchlist.medias == []


def test_watchlist_from_model(one_piece_anime_model, naruto_manga_model, mocker):
    mock_watchlist_model = mocker.Mock()
    mock_watchlist_model.name = "Liste"
    mock_watchlist_model.medias.all = lambda: [
        one_piece_anime_model,
        naruto_manga_model,
    ]

    mock_anime_from_model = mocker.patch(
        "tracking.domain.anime.Anime.from_model",
        side_effect=lambda anime_model: f"from_model({anime_model.title})",
    )
    mock_manga_from_model = mocker.patch(
        "tracking.domain.manga.Manga.from_model",
        side_effect=lambda manga_model: f"from_model({manga_model.title})",
    )
    watchlist = Watchlist.from_model(mock_watchlist_model)

    assert isinstance(watchlist, Watchlist)
    assert watchlist.name == "Liste"
    assert watchlist.medias == ["from_model(One Piece)", "from_model(Naruto)"]
    mock_anime_from_model.assert_called_once()
    mock_manga_from_model.assert_called_once()


# TEST IMAGESURLS
#######################################################


def test_images_urls_from_schema(mocker):
    images_urls_schema = mocker.Mock()
    images_urls_schema.small_image_url = "http://url_small_image.com"
    images_urls_schema.image_url = "http://url_medium_image.com"
    images_urls_schema.large_image_url = "http://url_large_image.com"

    image_urls = ImagesUrls.from_schema(images_urls_schema)
    assert isinstance(image_urls, ImagesUrls)
    assert image_urls.small_image_url == "http://url_small_image.com"
    assert image_urls.medium_image_url == "http://url_medium_image.com"
    assert image_urls.large_image_url == "http://url_large_image.com"


def test_images_urls_from_schema_none_value(mocker):
    images_urls_schema = mocker.Mock()
    images_urls_schema.small_image_url = None
    images_urls_schema.image_url = None
    images_urls_schema.large_image_url = None

    images_urls = ImagesUrls.from_schema(images_urls_schema)
    assert isinstance(images_urls, ImagesUrls)
    assert images_urls.small_image_url is None
    assert images_urls.medium_image_url is None
    assert images_urls.large_image_url is None


"""
def test_images_urls_from_model(mocker):
    images_urls_model = mocker.Mock()
    images_urls_model.small_image_url = "http://url_small_image.com"
    images_urls_model.medium_image_url = "http://url_medium_image.com"
    images_urls_model.large_image_url = "http://url_large_image.com"

    image_urls = ImagesUrls.from_model(images_urls_model)
    assert isinstance(image_urls, ImagesUrls)
    assert image_urls.small_image_url == "http://url_small_image.com"
    assert image_urls.medium_image_url == "http://url_medium_image.com"
    assert image_urls.large_image_url == "http://url_large_image.com"


def test_images_urls_from_model_none_value(mocker):
    images_urls_model = mocker.Mock()
    images_urls_model.small_image_url = ""
    images_urls_model.medium_image_url = ""
    images_urls_model.large_image_url = ""

    image_urls = ImagesUrls.from_model(images_urls_model)
    assert isinstance(image_urls, ImagesUrls)
    assert image_urls.small_image_url is None
    assert image_urls.medium_image_url is None
    assert image_urls.large_image_url is None

"""

# TESTS MEDIA
###########################################################


def test_base_fields_from_schema_one_piece_anime_full_schema(
    mocker, one_piece_anime_schema
):
    media_schema = one_piece_anime_schema
    mock_genre_from_schema = mocker.patch(
        "tracking.domain.media.Genre.from_schema",
        side_effect=lambda genre_schema: f"from_schema({genre_schema.name})",
    )
    mock_theme_from_schema = mocker.patch(
        "tracking.domain.media.Theme.from_schema",
        side_effect=lambda theme_schema: f"from_schema({theme_schema.name})",
    )
    mock_demographic_from_schema = mocker.patch(
        "tracking.domain.media.Demographic.from_schema",
        side_effect=lambda demographic_schema: f"from_schema({demographic_schema.name})",
    )
    data = Media._base_fields_from_schema(media_schema)
    assert data["mal_id"] == 17
    assert data["title"] == "One Piece"
    assert data["score"] == 8.73
    assert data["synopsis"] == media_schema.synopsis
    assert data["number_sections"] is None
    assert data["rank"] == 54
    assert data["status"] == "Currently Airing"
    assert data["user_score"] is None
    assert data["user_completion"] == MediaStatus.NOT_STARTED
    assert data["user_current_section"] == 0
    assert data["genres"] == [
        "from_schema(Action)",
        "from_schema(Adventure)",
        "from_schema(Fantasy)",
    ]
    assert data["themes"] == []
    assert data["demographics"] == ["from_schema(Shounen)"]
    assert len(data.items()) == 14


def test_base_fields_from_schema_naruto_manga_full_schema(mocker, naruto_manga_schema):
    media_schema = naruto_manga_schema
    mock_genre_from_schema = mocker.patch(
        "tracking.domain.media.Genre.from_schema",
        side_effect=lambda genre_schema: f"from_schema({genre_schema.name})",
    )
    mock_theme_from_schema = mocker.patch(
        "tracking.domain.media.Theme.from_schema",
        side_effect=lambda theme_schema: f"from_schema({theme_schema.name})",
    )
    mock_demographic_from_schema = mocker.patch(
        "tracking.domain.media.Demographic.from_schema",
        side_effect=lambda demographic_schema: f"from_schema({demographic_schema.name})",
    )
    data = Media._base_fields_from_schema(media_schema)
    assert data["mal_id"] == 11
    assert data["title"] == "Naruto"
    assert data["score"] == 8.08
    assert data["synopsis"] == media_schema.synopsis
    assert data["number_sections"] == 72
    assert data["rank"] == 698
    assert data["status"] == "Finished"
    assert data["user_score"] is None
    assert data["user_completion"] == MediaStatus.NOT_STARTED
    assert data["user_current_section"] == 0
    assert data["genres"] == [
        "from_schema(Action)",
        "from_schema(Adventure)",
        "from_schema(Fantasy)",
    ]
    assert data["themes"] == ["from_schema(Martial Arts)"]
    assert data["demographics"] == ["from_schema(Shounen)"]
    assert len(data.items()) == 14


def test_base_fields_from_schema_one_piece_anime_model(
    mocker, one_piece_anime_model, db
):
    media_model = one_piece_anime_model
    mock_genre_from_model = mocker.patch(
        "tracking.domain.media.Genre.from_model",
        side_effect=lambda genre_model: f"from_model({genre_model.name})",
    )
    mock_theme_from_model = mocker.patch(
        "tracking.domain.media.Theme.from_model",
        side_effect=lambda theme_model: f"from_model({theme_model.name})",
    )
    mock_demographic_from_model = mocker.patch(
        "tracking.domain.media.Demographic.from_model",
        side_effect=lambda demographic_model: f"from_model({demographic_model.name})",
    )
    data = Media._base_fields_from_model(media_model)
    assert data["mal_id"] == 17
    assert data["images_urls"].small_image_url == media_model.small_image_url
    assert data["images_urls"].medium_image_url == media_model.image_url
    assert data["images_urls"].large_image_url == media_model.large_image_url
    assert data["title"] == "One Piece"
    assert data["score"] == 8.73
    assert data["synopsis"] == media_model.synopsis
    assert data["number_sections"] is None
    assert data["rank"] == 54
    assert data["themes"] == []
    assert data["genres"] == [
        "from_model(Action)",
        "from_model(Adventure)",
        "from_model(Fantasy)",
    ]
    assert data["demographics"] == ["from_model(Shounen)"]
    assert data["status"] == "Currently Airing"
    assert data["user_score"] is None
    assert data["user_completion"] == MediaStatus.NOT_STARTED
    assert data["user_current_section"] == 0
    assert len(data.items()) == 14


def test_base_fields_from_model_naruto_manga_model(mocker, naruto_manga_model, db):
    media_model = naruto_manga_model
    mock_genre_from_model = mocker.patch(
        "tracking.domain.media.Genre.from_model",
        side_effect=lambda genre_model: f"from_model({genre_model.name})",
    )
    mock_theme_from_model = mocker.patch(
        "tracking.domain.media.Theme.from_model",
        side_effect=lambda theme_model: f"from_model({theme_model.name})",
    )
    mock_demographic_from_model = mocker.patch(
        "tracking.domain.media.Demographic.from_model",
        side_effect=lambda demographic_model: f"from_model({demographic_model.name})",
    )
    data = Media._base_fields_from_model(media_model)
    assert data["mal_id"] == 11
    assert data["title"] == "Naruto"
    assert data["score"] == 8.08
    assert data["synopsis"] == media_model.synopsis
    assert data["rank"] == 698
    assert data["status"] == "Finished"
    assert data["user_score"] is None
    assert data["user_completion"] == MediaStatus.NOT_STARTED
    assert data["user_current_section"] == 0
    assert data["genres"] == [
        "from_model(Action)",
        "from_model(Adventure)",
        "from_model(Fantasy)",
    ]
    assert data["themes"] == ["from_model(Martial Arts)"]
    assert data["demographics"] == ["from_model(Shounen)"]
    assert len(data.items()) == 14
