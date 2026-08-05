from dataclasses import dataclass

from .domain.anime import Anime
from .domain.manga import Manga
from .domain.media import Media
from .enums import MediaType
from .models.anime_models import AnimeModel
from .models.manga_models import MangaModel
from .models.media_models import MediaModel


@dataclass(frozen=True)
class MediaMapping:
    media_type: MediaType
    domain: type[Media]
    model: type[MediaModel]


MEDIA_MAPPINGS = (
    MediaMapping(MediaType.ANIME, Anime, AnimeModel),
    MediaMapping(MediaType.MANGA, Manga, MangaModel),
)

DOMAIN_TO_MODEL = {m.domain: m.model for m in MEDIA_MAPPINGS}
MODEL_TO_DOMAIN = {m.model: m.domain for m in MEDIA_MAPPINGS}
TYPE_TO_DOMAIN = {m.media_type: m.domain for m in MEDIA_MAPPINGS}
TYPE_TO_MODEL = {m.media_type: m.model for m in MEDIA_MAPPINGS}
