from ..domain.media import Media
from ..models.media_models import MediaModel
from ..services.integrations import jikan_services
from ..services.repositories import media_services
from ..forms import SectionNumberForm

def get_or_fetch_media(mal_id : int, media_type : str) -> Media:
    try:
        return media_services.get_media(mal_id = mal_id, media_type=media_type)
    except ValueError:
        return jikan_services.get_media_full(mal_id, media_type)

def get_or_import_media(mal_id : int, media_type : str) -> Media:
    try:
        return media_services.get_media(mal_id = mal_id, media_type=media_type)
    except ValueError:
        media = jikan_services.get_media_full(mal_id, media_type)
        return media_services.create_media(media)

def get_ongoing_medias() ->list[Media]:
    return media_services.get_medias(user_completion = "Ongoing")

def get_finished_medias() ->list[Media]:
    return media_services.get_medias(user_completion = "Finished")

def get_unseen_medias() ->list[Media]:
    return media_services.get_medias(user_completion = "Unseen")

def get_section_number_form(mal_id : int, media_type : str) -> SectionNumberForm | None:
    media = get_or_fetch_media(mal_id, media_type)
    if media.number_sections is None:
        return None
    return SectionNumberForm(media.number_sections)