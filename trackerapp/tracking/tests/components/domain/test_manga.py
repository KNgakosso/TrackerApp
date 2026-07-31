from tracking.domain.manga import Author, Manga
from tracking.tests.data.authors_data import INOUE_TAKHEHIKO, KISHIMOTO_MASASHI
from tracking.tests.data.manga_data import NARUTO_MANGA, SLAM_DUNK_MANGA

# TEST AUTHOR : FROM_SCHEMA
###########################################################


def test_author_from_schema_inoue_takehiko(author_schema_example):
    inoue_takehiko_schema = author_schema_example(**INOUE_TAKHEHIKO)
    author = Author.from_schema(inoue_takehiko_schema)
    assert isinstance(author, Author)
    assert author.name == "Inoue, Takehiko"
    assert author.mal_id == 1911


# TEST AUTHOR : FROM_MODEL
###########################################################


def test_author_from_schema_kishimoto_masashi(author_model_example):
    inoue_takehiko_model = author_model_example(**KISHIMOTO_MASASHI)
    author = Author.from_model(inoue_takehiko_model)
    assert isinstance(author, Author)
    assert author.name == "Kishimoto, Masashi"
    assert author.mal_id == 1879


# TESTS MANGA : FROM_SCHEMA
###########################################################


def test_manga_from_schema_slam_dunk(mocker, manga_schema_example):
    slam_dunk_schema = manga_schema_example(**SLAM_DUNK_MANGA)

    manga = Manga.from_schema(slam_dunk_schema)
    assert isinstance(manga, Manga)
    assert manga.chapters == 276
    assert len(manga.authors) == 1
    assert isinstance(manga.authors[0], Author)
    assert manga.authors[0].name == "Inoue, Takehiko"


def test_manga_from_schema_empty(mocker, manga_schema_example):
    manga_schema_empty = manga_schema_example(chapters=None, authors=[])

    manga = Manga.from_schema(manga_schema_empty)
    assert isinstance(manga, Manga)
    assert manga.chapters is None
    assert len(manga.authors) == 0


# TESTS MANGA : FROM_MODEL
###########################################################


def test_manga_from_model_naruto(manga_model_example):
    naruto_model = manga_model_example(**NARUTO_MANGA)

    manga = Manga.from_model(naruto_model)
    assert isinstance(manga, Manga)
    assert manga.chapters == 700
    assert len(manga.authors) == 1
    assert isinstance(manga.authors[0], Author)
    assert manga.authors[0].name == "Kishimoto, Masashi"


def test_manga_from_model_empty(manga_model_example):
    manga_model_empty = manga_model_example(chapters=None, authors=[])

    manga = Manga.from_model(manga_model_empty)
    assert isinstance(manga, Manga)
    assert manga.chapters is None
    assert len(manga.authors) == 0
