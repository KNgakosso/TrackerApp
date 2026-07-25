from tracking.domain.enums import AnimeRating


def test_age_rating_filter_value():
    rating = AnimeRating.PG13
    assert rating.filter_value == "pg13"


def test_age_rating_display():
    rating = AnimeRating.RPLUS
    assert rating.display == "Nudité"
