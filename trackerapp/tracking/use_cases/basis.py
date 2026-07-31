from ..domain.media import Media
from ..enums import MediaCompletion
from ..forms import SectionNumberForm
from ..services.api.tenrai import tenrai_services
from ..services.storage import storage_services


def get_or_fetch_media(mal_id: int, media_type: str) -> Media:
    try:
        return storage_services.get_media(mal_id=mal_id, media_type=media_type)
    except ValueError:
        return tenrai_services.get_media_full(mal_id, media_type)


def get_or_import_media(mal_id: int, media_type: str) -> Media:
    try:
        return storage_services.get_media(mal_id=mal_id, media_type=media_type)
    except ValueError:
        media = tenrai_services.get_media_full(mal_id, media_type)
        return storage_services.create_media(media)


def get_ongoing_medias() -> list[Media]:
    return storage_services.get_medias(user_completion=MediaCompletion.IN_PROGRESS)


def get_finished_medias() -> list[Media]:
    return storage_services.get_medias(user_completion=MediaCompletion.COMPLETED)


def get_unseen_medias() -> list[Media]:
    return storage_services.get_medias(user_completion=MediaCompletion.NOT_STARTED)


def get_section_number_form(mal_id: int, media_type: str) -> SectionNumberForm | None:
    media = get_or_fetch_media(mal_id, media_type)
    if media.number_sections is None:
        return None
    return SectionNumberForm(media.number_sections)
