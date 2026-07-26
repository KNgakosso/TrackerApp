from ...domain.enums import AnimeRating, MediaCompletion, MediaStatus
from .categories_data import (
    ACTION_GENRE,
    ADVENTURE_GENRE,
    FANTASY_GENRE,
    SHOUNEN_DEMOGRAPHIC,
)
from .studios_data import MADHOUSE, TOEI_ANIMATION

ONE_PIECE_ANIME = {
    "mal_id": 21,
    "title": "One Piece",
    "small_image_url": "https://cdn.myanimelist.net/images/anime/1244/138851t.webp",
    "image_url": "https://cdn.myanimelist.net/images/anime/1244/138851.webp",
    "large_image_url": "https://cdn.myanimelist.net/images/anime/1244/138851l.webp",
    "format": "TV",
    "synopsis": "Barely surviving in a barrel after passing through a terrible whirlpool at sea, carefree Monkey D. Luffy ends up aboard a ship under attack by fearsome pirates. Despite being a naive-looking teenager, he is not to be underestimated. Unmatched in battle, Luffy is a pirate himself who resolutely pursues the coveted One Piece treasure and the King of the Pirates title that comes with it.\n\nThe late King of the Pirates, Gol D. Roger, stirred up the world before his death by disclosing the whereabouts of his hoard of riches and daring everyone to obtain it. Ever since then, countless powerful pirates have sailed dangerous seas for the prized One Piece only to never return. Although Luffy lacks a crew and a proper ship, he is endowed with a superhuman ability and an unbreakable spirit that make him not only a formidable adversary but also an inspiration to many.\n\nAs he faces numerous challenges with a big smile on his face, Luffy gathers one-of-a-kind companions to join him in his ambitious endeavor, together embracing perils and wonders on their once-in-a-lifetime adventure",
    "score": 8.73,
    "rank": 54,
    "status": MediaStatus.CURRENTLY_AIRING,
    "themes": [],
    "genres": [
        ACTION_GENRE,
        ADVENTURE_GENRE,
        FANTASY_GENRE,
    ],
    "demographics": [SHOUNEN_DEMOGRAPHIC],
    "number_sections": None,
    "studios": [TOEI_ANIMATION],
    "duration": "23 min per ep",
    "rating": AnimeRating.PG13,
    "user_score": 8,
    "user_completion": MediaCompletion.IN_PROGRESS,
    "user_current_section": None,
}

HUNTER_X_HUNTER_ANIME = {
    "mal_id": 11061,
    "title": "Hunter x Hunter (2011)",
    "small_image_url": "https://cdn.myanimelist.net/images/anime/1337/99013t.webp",
    "image_url": "https://cdn.myanimelist.net/images/anime/1337/99013.webp",
    "large_image_ur": "https://cdn.myanimelist.net/images/anime/1337/99013l.webp",
    "format": "TV",
    "synopsis": "Hunters devote themselves to accomplishing hazardous tasks, all from traversing the world's uncharted territories to locating rare items and monsters. Before becoming a Hunter, one must pass the Hunter Examination—a high-risk selection process in which most applicants end up handicapped or worse, deceased.\n\nAmbitious participants who challenge the notorious exam carry their own reason. What drives 12-year-old Gon Freecss is finding Ging, his father and a Hunter himself. Believing that he will meet his father by becoming a Hunter, Gon takes the first step to walk the same path.\n\nDuring the Hunter Examination, Gon befriends the medical student Leorio Paladiknight, the vindictive Kurapika, and ex-assassin Killua Zoldyck. While their motives vastly differ from each other, they band together for a common goal and begin to venture into a perilous world.",
    "score": 9.03,
    "rank": 10,
    "status": MediaStatus.FINISHED_AIRING,
    "themes": [],
    "genres": [
        ACTION_GENRE,
        ADVENTURE_GENRE,
        FANTASY_GENRE,
    ],
    "demographics": [SHOUNEN_DEMOGRAPHIC],
    "number_sections": 148,
    "studios": [MADHOUSE],
    "duration": "23 min per ep",
    "rating": AnimeRating.PG13,
    "user_score": 10,
    "user_completion": MediaCompletion.COMPLETED,
    "user_current_section": 148,
}
