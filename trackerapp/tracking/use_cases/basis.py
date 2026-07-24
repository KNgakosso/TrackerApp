from ..domain.enums import MediaCompletion
from ..domain.media import Media
from ..forms import SectionNumberForm
from ..services.integrations import jikan_services
from ..services.repositories import media_services


def get_or_fetch_media(mal_id: int, media_type: str) -> Media:
    try:
        return media_services.get_media(mal_id=mal_id, media_type=media_type)
    except ValueError:
        return jikan_services.get_media_full(mal_id, media_type)


def get_or_import_media(mal_id: int, media_type: str) -> Media:
    try:
        return media_services.get_media(mal_id=mal_id, media_type=media_type)
    except ValueError:
        media = jikan_services.get_media_full(mal_id, media_type)
        return media_services.create_media(media)


def get_ongoing_medias() -> list[Media]:
    return media_services.get_medias(user_completion=MediaCompletion.IN_PROGRESS)


def get_finished_medias() -> list[Media]:
    return media_services.get_medias(user_completion=MediaCompletion.COMPLETED)


def get_unseen_medias() -> list[Media]:
    return media_services.get_medias(user_completion=MediaCompletion.NOT_STARTED)


def get_section_number_form(mal_id: int, media_type: str) -> SectionNumberForm | None:
    media = get_or_fetch_media(mal_id, media_type)
    if media.number_sections is None:
        return None
    return SectionNumberForm(media.number_sections)
