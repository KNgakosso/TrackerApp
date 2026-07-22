from typing import Callable

import pytest

from tracking.external.schemas.anime_schemas import AnimeFullSchema, StudioSchema
from tracking.external.schemas.enums import AgeRating
from tracking.external.schemas.manga_schemas import AuthorSchema, MangaFullSchema
from tracking.external.schemas.media_schemas import (
    DemographicSchema,
    GenreSchema,
    ImagesSchema,
    ImagesUrlsSchema,
    ThemeSchema,
)
from tracking.models.anime_models import AnimeModel
from tracking.models.manga_models import MangaModel
from tracking.models.media_models import MediaModelStatus

AnimeModelMaker = Callable[[], AnimeModel]
MangaModelMaker = Callable[[], MangaModel]
AnimeSchemaMaker = Callable[[], AnimeFullSchema]
MangaSchemaMaker = Callable[[], MangaFullSchema]


@pytest.fixture()
def manga_model_example() -> MangaModelMaker:
    def make_manga_model(
        mal_id: int = 0,
        title: str = "Un Manga",
        user_score: int = 6,
        user_completion: MediaModelStatus = MediaModelStatus.IN_PROGRESS,
        user_current_section: int = 10,
        score: float = 4.3,
        synopsis="Exemple de synopsis.",
        number_sections: int = 25,
        rank: int = 78,
        status: str = "Finished",
        number_volumes: int = 25,
        small_image_url: str = "https:///images/manga/mal_id/small.webp",
        medium_image_url: str = "https:///images/manga/mal_id/medium.webp",
        large_image_url: str = "https:///images/manga/mal_id/large.webp",
    ) -> MangaModel:
        manga_model = MangaModel(
            mal_id=mal_id,
            title=title,
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
            score=score,
            synopsis=synopsis,
            number_sections=number_sections,
            rank=rank,
            status=status,
            number_volumes=number_volumes,
            small_image_url=small_image_url,
            medium_image_ur=medium_image_url,
            large_image_ur=large_image_url,
        )
        return manga_model

    return make_manga_model


@pytest.fixture()
def manga_schema_example() -> MangaSchemaMaker:
    def make_manga_schema(
        mal_id: int = 0,
        title: str = "Un Manga",
        score: float = 4.3,
        synopsis="Exemple de synopsis.",
        number_sections: int = 25,
        rank: int = 78,
        status: str = "Finished",
        small_image_url: str = "https:///images/manga/mal_id/small.webp",
        image_url: str = "https:///images/manga/mal_id/medium.webp",
        large_image_url: str = "https:///images/manga/mal_id/large.webp",
    ) -> MangaFullSchema:
        manga_schema = MangaFullSchema(
            mal_id=mal_id,
            images=ImagesSchema(
                webp=ImagesUrlsSchema(
                    small_image_url=small_image_url,
                    image_url=image_url,
                    large_image_url=large_image_url,
                ),
                jpg=ImagesUrlsSchema(
                    small_image_url=None, image_url=None, large_image_url=None
                ),
            ),
            format="format",
            title=title,
            score=score,
            synopsis=synopsis,
            number_sections=number_sections,
            rank=rank,
            themes=[],
            genres=[],
            demographics=[],
            status=status,
            chapters=10000,
            authors=[],
        )
        return manga_schema

    return make_manga_schema


@pytest.fixture()
def anime_model_example() -> AnimeModelMaker:
    def make_anime_model(
        mal_id: int = 0,
        title: str = "Un Animé",
        user_score: int = 6,
        user_completion: MediaModelStatus = MediaModelStatus.IN_PROGRESS,
        user_current_section: int = 10,
        score: float = 4.3,
        synopsis="Exemple de synopsis.",
        number_sections: int = 25,
        rank: int = 78,
        status: str = "Finished",
        rating: str = "pg13",
        number_episodes: int = 25,
        number_seasons: int = 1,
    ) -> AnimeModel:
        anime_model = AnimeModel(
            mal_id=mal_id,
            title=title,
            user_score=user_score,
            user_completion=user_completion,
            user_current_section=user_current_section,
            score=score,
            synopsis=synopsis,
            number_sections=number_sections,
            rank=rank,
            status=status,
            rating=rating,
            number_episodes=number_episodes,
            number_seasons=number_seasons,
        )
        return anime_model

    return make_anime_model


@pytest.fixture()
def anime_schema_example() -> AnimeSchemaMaker:
    def make_anime_schema(
        mal_id: int = 0,
        title: str = "Un Anime",
        score: float = 4.3,
        synopsis="Exemple de synopsis.",
        number_sections: int = 25,
        rank: int = 78,
        status: str = "Finished",
        small_image_url: str = "https:///images/anime/mal_id/small.webp",
        image_url: str = "https:///images/anime/mal_id/medium.webp",
        large_image_url: str = "https:///images/anime/mal_id/large.webp",
        studios=[],
        duration="24 min",
        rating=AgeRating.G,
    ) -> AnimeFullSchema:
        anime_schema = AnimeFullSchema(
            mal_id=mal_id,
            images=ImagesSchema(
                webp=ImagesUrlsSchema(
                    small_image_url=small_image_url,
                    image_url=image_url,
                    large_image_url=large_image_url,
                ),
                jpg=ImagesUrlsSchema(
                    small_image_url=None, image_url=None, large_image_url=None
                ),
            ),
            format="format",
            title=title,
            score=score,
            synopsis=synopsis,
            number_sections=number_sections,
            rank=rank,
            themes=[],
            genres=[],
            demographics=[],
            status=status,
            studios=studios,
            duration=duration,
            rating=rating,
        )
        return anime_schema

    return make_anime_schema


@pytest.fixture()
def one_piece_anime_model() -> AnimeModel:
    return AnimeModel(
        mal_id=21,
        title="One Piece",
        user_score=8,
        user_completion=MediaModelStatus.IN_PROGRESS,
        user_current_section=190,
        score=8.73,
        synopsis="Barely surviving in a barrel after passing through a terrible whirlpool at sea, carefree Monkey D. Luffy ends up aboard a ship under attack by fearsome pirates. Despite being a naive-looking teenager, he is not to be underestimated. Unmatched in battle, Luffy is a pirate himself who resolutely pursues the coveted One Piece treasure and the King of the Pirates title that comes with it.\n\nThe late King of the Pirates, Gol D. Roger, stirred up the world before his death by disclosing the whereabouts of his hoard of riches and daring everyone to obtain it. Ever since then, countless powerful pirates have sailed dangerous seas for the prized One Piece only to never return. Although Luffy lacks a crew and a proper ship, he is endowed with a superhuman ability and an unbreakable spirit that make him not only a formidable adversary but also an inspiration to many.\n\nAs he faces numerous challenges with a big smile on his face, Luffy gathers one-of-a-kind companions to join him in his ambitious endeavor, together embracing perils and wonders on their once-in-a-lifetime adventure",
        number_sections=1250,
        rank=54,
        status="Currently Airing",
        rating="pg13",
        number_episodes=None,
        small_image_url="https:\/\/cdn.myanimelist.net\/images\/anime\/1244\/138851t.webp",
        medium_image_url="https:\/\/cdn.myanimelist.net\/images\/anime\/1244\/138851.webp",
        large_image_url="https:\/\/cdn.myanimelist.net\/images\/anime\/1244\/138851l.webp",
    )


@pytest.fixture()
def one_piece_anime_schema() -> AnimeFullSchema:
    return AnimeFullSchema(
        mal_id=17,
        images=ImagesSchema(
            webp=ImagesUrlsSchema(
                small_image_url="https:\/\/cdn.myanimelist.net\/images\/anime\/1244\/138851t.webp",
                image_url="https:\/\/cdn.myanimelist.net\/images\/anime\/1244\/138851.webp",
                large_image_url="https:\/\/cdn.myanimelist.net\/images\/anime\/1244\/138851l.webp",
            ),
            jpg=ImagesUrlsSchema(
                small_image_url=None, image_url=None, large_image_url=None
            ),
        ),
        format="TV",
        title="One Piece",
        score=8.73,
        synopsis="Barely surviving in a barrel after passing through a terrible whirlpool at sea, carefree Monkey D. Luffy ends up aboard a ship under attack by fearsome pirates. Despite being a naive-looking teenager, he is not to be underestimated. Unmatched in battle, Luffy is a pirate himself who resolutely pursues the coveted One Piece treasure and the King of the Pirates title that comes with it.\n\nThe late King of the Pirates, Gol D. Roger, stirred up the world before his death by disclosing the whereabouts of his hoard of riches and daring everyone to obtain it. Ever since then, countless powerful pirates have sailed dangerous seas for the prized One Piece only to never return. Although Luffy lacks a crew and a proper ship, he is endowed with a superhuman ability and an unbreakable spirit that make him not only a formidable adversary but also an inspiration to many.\n\nAs he faces numerous challenges with a big smile on his face, Luffy gathers one-of-a-kind companions to join him in his ambitious endeavor, together embracing perils and wonders on their once-in-a-lifetime adventure",
        number_sections=None,
        rank=54,
        themes=[],
        genres=[
            GenreSchema(mal_id=1, name="Action"),
            GenreSchema(mal_id=2, name="Adventure"),
            GenreSchema(mal_id=10, name="Fantasy"),
        ],
        demographics=[DemographicSchema(mal_id=27, name="Shounen")],
        status="Currently Airing",
        studios=[StudioSchema(mal_id=18, name="Toei Animation")],
        duration="24 min",
        rating=AgeRating.PG13,
    )


@pytest.fixture()
def hunter_x_hunter_anime_model() -> AnimeModel:
    return AnimeModel(
        mal_id=11061,
        title="Hunter x hunter (2011)",
        user_score=10,
        user_completion=MediaModelStatus.COMPLETED,
        user_current_section=148,
        score=9.03,
        synopsis="Hunters devote themselves to accomplishing hazardous tasks, all from traversing the world's uncharted territories to locating rare items and monsters. Before becoming a Hunter, one must pass the Hunter Examination—a high-risk selection process in which most applicants end up handicapped or worse, deceased.\n\nAmbitious participants who challenge the notorious exam carry their own reason. What drives 12-year-old Gon Freecss is finding Ging, his father and a Hunter himself. Believing that he will meet his father by becoming a Hunter, Gon takes the first step to walk the same path.\n\nDuring the Hunter Examination, Gon befriends the medical student Leorio Paladiknight, the vindictive Kurapika, and ex-assassin Killua Zoldyck. While their motives vastly differ from each other, they band together for a common goal and begin to venture into a perilous world.",
        number_sections=148,
        rank=10,
        status="Finished Airing",
        rating="pg13",
        number_episodes=148,
        medium_image_url="https://cdn.myanimelist.net/images/anime/1337/99013.webp",
        small_image_url="https://cdn.myanimelist.net/images/anime/1337/99013t.webp",
        large_image_url="https://cdn.myanimelist.net/images/anime/1337/99013l.webp",
    )


@pytest.fixture()
def hunter_x_hunter_anime_schema() -> AnimeFullSchema:
    return AnimeFullSchema(
        mal_id=11061,
        images=ImagesSchema(
            webp=ImagesUrlsSchema(
                image_url="https://cdn.myanimelist.net/images/anime/1337/99013.webp",
                small_image_url="https://cdn.myanimelist.net/images/anime/1337/99013t.webp",
                large_image_url="https://cdn.myanimelist.net/images/anime/1337/99013l.webp",
            ),
            jpg=ImagesUrlsSchema(
                image_url="https://cdn.myanimelist.net/images/anime/1337/99013.jpg",
                small_image_url="https://cdn.myanimelist.net/images/anime/1337/99013t.jpg",
                large_image_url="https://cdn.myanimelist.net/images/anime/1337/99013l.jpg",
            ),
        ),
        format="TV",
        title="Hunter x Hunter (2011)",
        score=9.03,
        synopsis="Hunters devote themselves to accomplishing hazardous tasks, all from traversing the world's uncharted territories to locating rare items and monsters. Before becoming a Hunter, one must pass the Hunter Examination—a high-risk selection process in which most applicants end up handicapped or worse, deceased.\n\nAmbitious participants who challenge the notorious exam carry their own reason. What drives 12-year-old Gon Freecss is finding Ging, his father and a Hunter himself. Believing that he will meet his father by becoming a Hunter, Gon takes the first step to walk the same path.\n\nDuring the Hunter Examination, Gon befriends the medical student Leorio Paladiknight, the vindictive Kurapika, and ex-assassin Killua Zoldyck. While their motives vastly differ from each other, they band together for a common goal and begin to venture into a perilous world.",
        number_sections=148,
        rank=10,
        themes=[],
        genres=[
            GenreSchema(mal_id=1, name="Action"),
            GenreSchema(mal_id=2, name="Adventure"),
            GenreSchema(mal_id=10, name="Fantasy"),
        ],
        demographics=[DemographicSchema(mal_id=27, name="Shounen")],
        status="Finished Airing",
        studios=[StudioSchema(mal_id=11, name="Madhouse")],
        duration="23 min per ep",
        rating=AgeRating.PG13,
    )


@pytest.fixture()
def naruto_manga_model() -> MangaModel:
    return MangaModel(
        mal_id=11,
        title="Naruto",
        user_score=7,
        user_completion=MediaModelStatus.IN_PROGRESS,
        user_current_section=71,
        score=8.08,
        synopsis="Whenever Naruto Uzumaki proclaims that he will someday become the Hokage—a title bestowed upon the best ninja in the Village Hidden in the Leaves—no one takes him seriously. Since birth, Naruto has been shunned and ridiculed by his fellow villagers. But their contempt isn't because Naruto is loud-mouthed, mischievous, or because of his ineptitude in the ninja arts, but because there is a demon inside him. Prior to Naruto's birth, the powerful and deadly Nine-Tailed Fox attacked the village. In order to stop the rampage, the Fourth Hokage sacrificed his life to seal the demon inside the body of the newborn Naruto.\n\nAnd so when he is assigned to Team 7—along with his new teammates Sasuke Uchiha and Sakura Haruno, under the mentorship of veteran ninja Kakashi Hatake—Naruto is forced to work together with other people for the first time in his life. Through undergoing vigorous training and taking on challenging missions, Naruto must learn what it means to work in a team and carve his own route toward becoming a full-fledged ninja recognized by his village.",
        number_sections=72,
        rank=698,
        status="Finished",
        number_volumes=72,
    )


@pytest.fixture()
def naruto_manga_schema() -> MangaModel:
    return MangaModel(
        mal_id=11,
        title="Naruto",
        user_score=7,
        user_completion=MediaModelStatus.IN_PROGRESS,
        user_current_section=71,
        score=8.08,
        synopsis="Whenever Naruto Uzumaki proclaims that he will someday become the Hokage—a title bestowed upon the best ninja in the Village Hidden in the Leaves—no one takes him seriously. Since birth, Naruto has been shunned and ridiculed by his fellow villagers. But their contempt isn't because Naruto is loud-mouthed, mischievous, or because of his ineptitude in the ninja arts, but because there is a demon inside him. Prior to Naruto's birth, the powerful and deadly Nine-Tailed Fox attacked the village. In order to stop the rampage, the Fourth Hokage sacrificed his life to seal the demon inside the body of the newborn Naruto.\n\nAnd so when he is assigned to Team 7—along with his new teammates Sasuke Uchiha and Sakura Haruno, under the mentorship of veteran ninja Kakashi Hatake—Naruto is forced to work together with other people for the first time in his life. Through undergoing vigorous training and taking on challenging missions, Naruto must learn what it means to work in a team and carve his own route toward becoming a full-fledged ninja recognized by his village.",
        number_sections=72,
        rank=698,
        status="Finished",
        number_volumes=72,
        themes=[ThemeSchema(mal_id=17, name="Martial Arts")],
        genres=[
            GenreSchema(mal_id=1, name="Action"),
            GenreSchema(mal_id=2, name="Adventure"),
            GenreSchema(mal_id=10, name="Fantasy"),
        ],
        demographics=[DemographicSchema(mal_id=27, name="Shounen")],
        authors=[AuthorSchema(mal_id=1879, name="Kishimoto, Masashi")],
        chapters=700,
    )


@pytest.fixture()
def slam_dunk_manga_model() -> MangaModel:
    return MangaModel(
        mal_id=51,
        title="Slam Dunk",
        user_score=None,
        user_completion=MediaModelStatus.NOT_STARTED,
        user_current_section=0,
        score=9.09,
        synopsis='Hanamichi Sakuragi, a tall, boisterous teenager with flame-red hair and physical strength beyond his years, is eager to put an end to his rejection streak of 50 and finally score a girlfriend as he begins his first year of Shohoku High. However, his reputation for delinquency and destructiveness precedes him, and most of his fellow students subsequently avoid him like the plague. As his first day of school ends, he is left with two strong thoughts: "I hate basketball" and "I need a girlfriend."\n\nHaruko Akagi, ignorant of Hanamichi\'s history of misbehavior, notices his immense height and unwittingly approaches him, asking whether or not he likes basketball. Overcome by the fact that a girl is speaking to him, the red-haired giant blurts out a yes despite his true feelings. At the gym, Haruko asks if he can do a slam dunk. Though a complete novice, Hanamachi palms the ball and makes the leap...but overshoots, slamming his head into the backboard. Amazed by his near-inhuman physical abilities, Haruko quickly notifies the school\'s basketball captain of his feat. With this, Hanamichi is unexpectedly thrust into a world of competition for a girl he barely knows, but he soon discovers that there is perhaps more to basketball than he once thought',
        number_sections=31,
        rank=7,
        status="Finished",
        number_volumes=31,
    )


@pytest.fixture()
def slam_dunk_manga_schema() -> MangaFullSchema:
    return MangaFullSchema(
        mal_id=51,
        images=ImagesSchema(
            webp=ImagesUrlsSchema(
                image_url="https://cdn.myanimelist.net/images/manga/2/258749.webp",
                small_image_url="https://cdn.myanimelist.net/images/manga/2/258749t.webp",
                large_image_url="https://cdn.myanimelist.net/images/manga/2/258749l.webp",
            ),
            jpg=ImagesUrlsSchema(
                image_url="https://cdn.myanimelist.net/images/manga/2/258749.jpg",
                small_image_url="https://cdn.myanimelist.net/images/manga/2/258749t.jpg",
                large_image_url="https://cdn.myanimelist.net/images/manga/2/258749l.jpg",
            ),
        ),
        format="Manga",
        title="Slam Dunk",
        score=9.09,
        synopsis='Hanamichi Sakuragi, a tall, boisterous teenager with flame-red hair and physical strength beyond his years, is eager to put an end to his rejection streak of 50 and finally score a girlfriend as he begins his first year of Shohoku High. However, his reputation for delinquency and destructiveness precedes him, and most of his fellow students subsequently avoid him like the plague. As his first day of school ends, he is left with two strong thoughts: "I hate basketball" and "I need a girlfriend."\n\nHaruko Akagi, ignorant of Hanamichi\'s history of misbehavior, notices his immense height and unwittingly approaches him, asking whether or not he likes basketball. Overcome by the fact that a girl is speaking to him, the red-haired giant blurts out a yes despite his true feelings. At the gym, Haruko asks if he can do a slam dunk. Though a complete novice, Hanamachi palms the ball and makes the leap...but overshoots, slamming his head into the backboard. Amazed by his near-inhuman physical abilities, Haruko quickly notifies the school\'s basketball captain of his feat. With this, Hanamichi is unexpectedly thrust into a world of competition for a girl he barely knows, but he soon discovers that there is perhaps more to basketball than he once thought',
        number_sections=31,
        rank=7,
        themes=[
            ThemeSchema(mal_id=23, name="School"),
            ThemeSchema(mal_id=78, name="Team Sports"),
        ],
        genres=[
            GenreSchema(mal_id=46, name="Award Winning"),
            GenreSchema(mal_id=30, name="Sports"),
        ],
        demographics=[DemographicSchema(mal_id=27, name="Shounen")],
        status="Finished",
        authors=[AuthorSchema(mal_id=1911, name="Inoue, Takehiko")],
        chapters=276,
    )
