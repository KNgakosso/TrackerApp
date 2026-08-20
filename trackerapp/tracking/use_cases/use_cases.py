from django.utils.translation import get_language

from ..domain.media import Media
from ..domain.watchlist import Watchlist
from ..enums import MediaType
from ..forms import ScoreForm, SectionNumberForm, WatchlistForm
from ..services.storage import storage_services
from . import basis


def create_watchlist(watchlist_form: WatchlistForm) -> Watchlist:
    name = watchlist_form.cleaned_data["name"]
    watchlist = Watchlist(name=name, medias=[])
    storage_services.save_watchlist(watchlist=watchlist)
    return watchlist


def add_media_to_watchlist(
    watchlist_name: str, media_mal_id: int, media_type: MediaType
) -> Watchlist:
    watchlist = storage_services.get_watchlist(name=watchlist_name)
    media = basis.get_or_import_media(media_mal_id, media_type)
    watchlist.medias.append(media)
    storage_services.save_watchlist(watchlist)
    return storage_services.get_watchlist(watchlist_name)


def remove_media_from_watchlist(
    watchlist_name: str, media_mal_id: int, media_type: MediaType
) -> Watchlist:
    watchlist = storage_services.get_watchlist(name=watchlist_name)
    media = basis.get_or_import_media(media_mal_id, media_type)
    watchlist.medias.remove(media)
    storage_services.save_watchlist(watchlist)
    return storage_services.get_watchlist(watchlist_name)


def delete_watchlist(watchlist_name: str) -> list[Watchlist]:
    storage_services.delete_watchlist(name=watchlist_name)
    return storage_services.get_watchlists()


def complete_media_next_section(mal_id: int, media_type: MediaType) -> Media:
    media = basis.get_or_import_media(mal_id, media_type)
    media.complete_next()
    storage_services.save_media(media)
    return media


def set_media_current_user_section(
    mal_id: int, media_type: MediaType, section_number_form: SectionNumberForm
) -> Media:
    new_current_section = section_number_form.cleaned_data["section_number"]
    media = basis.get_or_import_media(mal_id, media_type)
    if (
        media.user_current_section is None
        or new_current_section > media.number_sections
    ):
        raise ValueError
    media.define_current_section(new_current_section)
    storage_services.save_media(media)
    return storage_services.get_media(mal_id=mal_id, media_type=media_type)


def finish_media(mal_id: int, media_type: MediaType) -> Media:
    media = basis.get_or_import_media(mal_id, media_type)
    media.complete()
    storage_services.save_media(media)

    return storage_services.get_media(mal_id=mal_id, media_type=media_type)


def set_media_user_score(
    mal_id: int, media_type: MediaType, score_form: ScoreForm
) -> Media:
    media = basis.get_or_import_media(mal_id, media_type)
    media.user_score = score_form.cleaned_data["score"]
    storage_services.save_media(media)

    return storage_services.get_media(mal_id=mal_id, media_type=media_type)


def rename_watchlist(name: str, watchlist_form: WatchlistForm) -> Watchlist:
    new_name = watchlist_form.cleaned_data["name"]
    storage_services.rename_watchlist(prev_name=name, new_name=new_name)
    return storage_services.get_watchlist(new_name)


def translate_synopsis(mal_id: int, media_type: MediaType):
    media = basis.get_or_fetch_media(mal_id, media_type)
    current_language = get_language()
    media.translate_synopsis(current_language)
    storage_services.save_if_stored_media(media)
    return media


"""
def set_section_user_score_2(media_mal_id : int, media_type : str, section_mal_id : int, score_form : ScoreForm) -> Media:
    section = basis.get_section(media_mal_id, media_type, section_mal_id)
    section.score = score_form.cleaned_data['score']
    return basis.update_section(section)
"""
