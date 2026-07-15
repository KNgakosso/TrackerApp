from ..models.media_models import MediaModel
from ..models.anime_models import AnimeModel
from ..models.manga_models import MangaModel
from ..domain.media import Media
from ..domain.anime import Anime
from ..domain.manga import Manga


DOMAIN_TO_MODEL = {
    Media: MediaModel,
    Anime: AnimeModel,
    Manga: MangaModel,
}

MODEL_TO_DOMAIN = {
    MangaModel: Manga,
    AnimeModel: Anime,
    MediaModel: Media
}

TYPE_TO_CLASS = {
    "manga": Manga,
    "anime": Anime,
    "media": Media
} 

TYPE_TO_MODEL = {
    "manga": MangaModel,
    "anime": AnimeModel,
    "media": MediaModel
} 