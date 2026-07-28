import pytest

from ..data.anime_data import HUNTER_X_HUNTER_ANIME, ONE_PIECE_ANIME
from ..data.manga_data import NARUTO_MANGA, SLAM_DUNK_MANGA
from .anime_maker import anime_model_example
from .manga_maker import manga_model_example


@pytest.fixture()
def db_example(anime_model_example, manga_model_example):
    hunter_x_hunter_anime_model = anime_model_example(**HUNTER_X_HUNTER_ANIME)
    one_piece_anime_model = anime_model_example(**ONE_PIECE_ANIME)
    slam_dunk_manga_model = manga_model_example(**SLAM_DUNK_MANGA)
    naruto_manga_model = manga_model_example(**NARUTO_MANGA)
