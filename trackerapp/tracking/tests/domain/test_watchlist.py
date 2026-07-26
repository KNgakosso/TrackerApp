from unittest.mock import patch

from tracking.domain.enums import AnimeRating, MediaCompletion, MediaStatus
from tracking.domain.media import Demographic, Genre, ImagesUrls, Media, Theme
from tracking.domain.watchlist import Watchlist
from tracking.models.watchlist_model import WatchlistModel
from tracking.tests.data.anime_data import HUNTER_X_HUNTER_ANIME, ONE_PIECE_ANIME
from tracking.tests.data.manga_data import NARUTO_MANGA, SLAM_DUNK_MANGA

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


def test_watchlist_from_model(
    anime_model_example,
    manga_model_example,
    mocker,
):
    mock_watchlist_model = mocker.Mock()
    mock_watchlist_model.name = "Liste"
    mock_watchlist_model.medias.all = lambda: [
        anime_model_example(**ONE_PIECE_ANIME),
        manga_model_example(**NARUTO_MANGA),
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
