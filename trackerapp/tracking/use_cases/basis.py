from ..domain.anime import Anime
from ..domain.media import Media
from ..enums import MediaCompletion, MediaType
from ..forms import SectionNumberForm
from ..services.api.tenrai import tenrai_services
from ..services.storage import storage_services


def get_or_fetch_media(mal_id: int, media_type: MediaType) -> Media:
    try:
        return storage_services.get_media(mal_id=mal_id, media_type=media_type)
    except ValueError:
        return tenrai_services.get_media_full(mal_id, media_type)


def get_or_import_media(mal_id: int, media_type: MediaType) -> Media:
    try:
        return storage_services.get_media(mal_id=mal_id, media_type=media_type)
    except ValueError:
        media = tenrai_services.get_media_full(mal_id, media_type)
        storage_services.save_media(media)
        return media


"""
def get_or_import_media(mal_id: int, media_type: MediaType) -> Media:
    media = Anime(
        mal_id=mal_id,
        title="Anime",
        images_urls=None,
        format=None,
        synopsis=None,
        score=None,
        rank=None,
        themes=[],
        genres=[],
        demographics=[],
        number_sections=500,
        status=None,
        user_score=None,
        user_completion=MediaCompletion.NOT_STARTED,
        user_current_section=0,
        studios=[],
        duration=None,
        rating=None,
    )
    media.number_sections = 500
    return media

"""


def get_ongoing_medias() -> list[Media]:
    return storage_services.get_medias(user_completion=MediaCompletion.IN_PROGRESS)


def get_finished_medias() -> list[Media]:
    return storage_services.get_medias(user_completion=MediaCompletion.COMPLETED)


def get_unseen_medias() -> list[Media]:
    return storage_services.get_medias(user_completion=MediaCompletion.NOT_STARTED)


def get_section_number_form_(
    mal_id: int, media_type: MediaType
) -> SectionNumberForm | None:
    media = get_or_fetch_media(mal_id, media_type)
    if media.number_sections is None:
        return None
    return SectionNumberForm(max_value=media.number_sections)


def get_section_number_form(media: Media) -> SectionNumberForm | None:
    if media.number_sections is None:
        return None
    return SectionNumberForm(max_value=media.number_sections)
