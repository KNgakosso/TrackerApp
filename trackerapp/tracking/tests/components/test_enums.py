import pytest
from tracking.enums import AnimeRating, MediaCompletion, MediaStatus

# ANIME RATING : FILTER_VALUE
#############################################


@pytest.mark.parametrize(
    ("rating", "filter_value"),
    [
        (AnimeRating.G, "g"),
        (AnimeRating.PG, "pg"),
        (AnimeRating.PG13, "pg13"),
        (AnimeRating.R17, "r17"),
        (AnimeRating.RPLUS, "r"),
        (AnimeRating.RX, "rx"),
    ],
)
def test_anime_rating_filter_value(rating, filter_value):
    assert rating.filter_value == filter_value


# ANIME RATING : DISPLAY
#############################################


@pytest.mark.parametrize(
    ("rating", "display"),
    [
        (AnimeRating.G, "All ages"),
        (AnimeRating.PG, "Young audience"),
        (AnimeRating.PG13, "13+"),
        (AnimeRating.R17, "Violence and profanity"),
        (AnimeRating.RPLUS, "Mild nudity"),
        (AnimeRating.RX, "Hentai"),
    ],
)
def test_anime_rating_display(rating, display):
    assert rating.display == display


# MEDIA STATUS : FILTER_VALUE
#############################################


@pytest.mark.parametrize(
    ("status", "filter_value"),
    [
        (MediaStatus.FINISHED, "complete"),
        (MediaStatus.PUBLISHING, "publishing"),
        (MediaStatus.HIATUS, "hiatus"),
        (MediaStatus.DISCONTINUED, "discontinued"),
        (MediaStatus.NOT_PUBLISHED, "upcoming"),
        (MediaStatus.FINISHED_AIRING, "complete"),
        (MediaStatus.CURRENTLY_AIRING, "airing"),
        (MediaStatus.NOT_AIRED, "upcoming"),
    ],
)
def test_media_status_filter_value(status, filter_value):
    assert status.filter_value == filter_value


# MEDIA STATUS : DISPLAY
#############################################


@pytest.mark.parametrize(
    ("status", "display"),
    [
        (MediaStatus.FINISHED, "Finished"),
        (MediaStatus.PUBLISHING, "Currently publishing"),
        (MediaStatus.HIATUS, "On hiatus"),
        (MediaStatus.DISCONTINUED, "Discontinued"),
        (MediaStatus.NOT_PUBLISHED, "Not yet published"),
        (MediaStatus.FINISHED_AIRING, "Finished airing"),
        (MediaStatus.CURRENTLY_AIRING, "Currently airing"),
        (MediaStatus.NOT_AIRED, "Not yet aired"),
    ],
)
def test_media_status_display(status, display):
    assert status.display == display


# MEDIA COMPLETION : DISPLAY
#############################################


@pytest.mark.parametrize(
    ("completion", "display"),
    [
        (MediaCompletion.NOT_STARTED, "Not started"),
        (MediaCompletion.IN_PROGRESS, "In progress"),
        (MediaCompletion.COMPLETED, "Completed"),
    ],
)
def test_media_completion_display(completion, display):
    assert completion.display == display
