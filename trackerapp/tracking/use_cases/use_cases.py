from ..domain.media import Media, MediaStatus
from ..domain.watchlist import Watchlist
from ..forms import ScoreForm, SectionNumberForm, WatchlistForm
from ..services.repositories import media_services, watchlist_services
from . import basis


def create_watchlist(watchlist_form: WatchlistForm) -> Watchlist:
    name = watchlist_form.cleaned_data["name"]
    watchlist = Watchlist(name=name, medias=[])
    watchlist_services.create_watchlist_model(watchlist=watchlist)
    return watchlist


def add_media_to_watchlist(
    watchlist_name: str, media_mal_id: int, media_type: str
) -> Watchlist:
    watchlist = watchlist_services.get_watchlist(name=watchlist_name)
    media = basis.get_or_import_media(media_mal_id, media_type)
    return watchlist_services.add_media_to_watchlist(watchlist, media)


def remove_media_from_watchlist(
    watchlist_name: str, media_mal_id: int, media_type: str
) -> Watchlist:
    watchlist = watchlist_services.get_watchlist(name=watchlist_name)
    media = basis.get_or_import_media(media_mal_id, media_type)
    return watchlist_services.remove_media_from_watchlist(watchlist, media)


def delete_watchlist(watchlist_name: str) -> list[Watchlist]:
    watchlist_services.delete_watchlist(name=watchlist_name)
    return watchlist_services.get_watchlists()


def update_completion(current_section: int, max_section: int):
    if current_section > max_section:
        raise ValueError
    elif current_section == max_section:
        return MediaStatus.COMPLETED
    elif current_section == 0:
        return MediaStatus.NOT_STARTED
    else:
        return MediaStatus.IN_PROGRESS


def complete_media_next_section(mal_id: int, media_type: str):
    media = basis.get_or_import_media(mal_id, media_type)
    if (
        media.number_sections is None
        or media.user_current_section == media.number_sections
    ):
        raise ValueError
    media.user_current_section += 1
    media.user_completion = update_completion(
        media.user_current_section, media.number_sections
    )
    return media_services.update_media(media)


def set_media_current_user_section(
    mal_id: int, media_type: str, section_number_form: SectionNumberForm
) -> Media:
    new_current_section = section_number_form.cleaned_data["section_number"]
    media = media_services.get_media(mal_id, media_type)
    if (
        media.user_current_section is None
        or new_current_section > media.user_current_section
    ):
        raise ValueError
    media.user_current_section = new_current_section
    media.user_completion = update_completion(
        media.user_current_section, media.user_current_section
    )
    return media_services.update_media(media)


def finish_media(mal_id: int, media_type: str) -> Media:
    media = basis.get_or_import_media(mal_id, media_type)
    media.user_current_section = media.number_sections
    media.user_completion = MediaStatus.COMPLETED
    return media_services.update_media(media)


def set_media_user_score(mal_id: int, media_type: str, score_form: ScoreForm) -> Media:
    media = media_services.get_media(mal_id, media_type)
    media.score = score_form.cleaned_data["score"]
    return media_services.update_media(media)


def rename_watchlist(name: str, watchlist_form: WatchlistForm) -> Watchlist:
    new_name = watchlist_form.cleaned_data["name"]
    watchlist_services.set_watchlist_name(prev_name=name, new_name=new_name)
    return watchlist_services.get_watchlist(new_name)


"""
def set_section_user_score_2(media_mal_id : int, media_type : str, section_mal_id : int, score_form : ScoreForm) -> Media:
    section = basis.get_section(media_mal_id, media_type, section_mal_id)
    section.score = score_form.cleaned_data['score']
    return basis.update_section(section)
"""
