from tracking.enums import AnimeRating

# TEST STUDIO : FROM_SCHEMA
###########################################################


def test_anime_from_schema_handle_none_rating_valid(anime_schema_example):
    anime_full_schema = anime_schema_example(rating="PG - Children")

    assert anime_full_schema.rating == AnimeRating.PG


def test_anime_from_schema_handle_none_rating_invalid(anime_schema_example):
    anime_full_schema = anime_schema_example(rating="Invalid Rating")

    assert anime_full_schema.rating is None
