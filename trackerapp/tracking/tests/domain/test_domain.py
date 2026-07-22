from unittest.mock import patch

from tracking.domain.media import Demographic, Genre, Images, ImagesUrls, Media, Theme
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


# TESTS IMAGES
###########################################


def test_images_from_schema(mocker):
    images_schema = mocker.Mock()
    images_schema.webp = "Images Urls Schema WEBP"
    images_schema.jpg = "Images Urls Schema JPG"

    mock_images_urls_from_model = mocker.patch(
        "tracking.domain.media.ImagesUrls.from_schema",
        side_effect=lambda x: f"From Schema ({x})",
    )
    images = Images.from_schema(images_schema)
    assert isinstance(images, Images)
    assert images.webp == "From Schema (Images Urls Schema WEBP)"
    assert images.jpg == "From Schema (Images Urls Schema JPG)"


def test_images_from_model(mocker):
    images_model = mocker.Mock()

    mock_images_urls_from_model = mocker.patch(
        "tracking.domain.media.ImagesUrls.from_model",
        side_effect=lambda x: ("From Model", x),
    )
    images = Images.from_model(images_model)
    assert isinstance(images, Images)
    assert images.webp == ("From Model", images_model)
    assert images.jpg is None
