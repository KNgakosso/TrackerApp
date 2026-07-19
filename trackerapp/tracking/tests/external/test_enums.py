from tracking.external.schemas.enums import AgeRating


def test_age_rating_filter_value():
    rating = AgeRating.PG13
    assert rating.filter_value == "pg13"


def test_age_rating_display():
    rating = AgeRating.RPLUS
    assert rating.display == "Nudité"
