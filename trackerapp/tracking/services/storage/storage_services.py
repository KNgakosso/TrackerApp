from ...domain.anime import Anime
from ...domain.manga import Manga
from ...domain.media import Demographic, Genre, Media, Theme
from ...domain.watchlist import Watchlist
from ...enums import MediaType
from ...exceptions import MediaNotFoundError, WatchlistNotFoundError
from ...models.repository import repository
from ...utils import TYPE_TO_DOMAIN

# GENRE STORAGE SERVICES
##############################################################


def get_genre(name: str) -> Genre:
    return Genre.from_model(repository.get_genre_model(name=name))


# THEME STORAGE SERVICES
##############################################################


def get_theme(name: str) -> Theme:
    return Theme.from_model(repository.get_theme_model(name=name))


# DEMOGRAPHIC STORAGE SERVICES
##############################################################


def get_demographic(name: str) -> Demographic:
    return Demographic.from_model(repository.get_demographic_model(name=name))


# MEDIA STORAGE SERVICES
##############################################################


def get_media(mal_id: int, media_type: MediaType) -> Media:
    media_class = TYPE_TO_DOMAIN[media_type]
    return media_class.from_model(
        repository.get_media_model(mal_id=mal_id, media_type=media_type)
    )


def get_medias(**kwargs) -> list[Media]:
    medias_models = repository.get_medias_models(**kwargs)
    medias = []
    for media_model in medias_models:
        media_class = TYPE_TO_DOMAIN[media_model.media_type]
        medias.append(media_class.from_model(media_model))
    return medias


"""
def update_media(media: Media):
    try:
        media_model = repository.get_media_model(media.mal_id, media.type())
        repository.set_media_model_user_completion(media_model, media.user_completion)
        repository.set_media_model_user_current_section(
            media_model, media.user_current_section
        )
        repository.set_media_model_user_score(media_model, media.user_score)
    except IntegrityError:
        raise ValueError(
            f"Mise à jour des données utilisateurs du média {media.mal_id} impossible."
        )
"""


def save_media(media: Media):
    try:
        media_model = repository.get_media_model(media.mal_id, media.media_type)
        repository.set_media_model_user_completion(media_model, media.user_completion)
        repository.set_media_model_user_current_section(
            media_model, media.user_current_section
        )
        repository.set_media_model_user_score(media_model, media.user_score)
    except MediaNotFoundError:
        repository.create_media_model(media)


def save_if_stored_media(media: Media):
    try:
        media_model = repository.get_media_model(media.mal_id, media.media_type)
        repository.set_media_model_synopsis_tanslated(
            media_model, media.synopsis_translated
        )
    except MediaNotFoundError:
        pass


"""
def set_media_user_completion(
    mal_id: int, media_type: str, new_completion: MediaCompletion
) -> str:
    media_model = repository.get_media_model(mal_id=mal_id, media_type=media_type)
    return repository.set_media_model_user_completion(media_model, new_completion)


def set_media_user_current_section(
    mal_id: int, media_type: str, new_current_section: int
) -> int | None:
    media_model = repository.get_media_model(mal_id=mal_id, media_type=media_type)
    return repository.set_media_model_user_current_section(
        media_model, new_current_section
    )
"""

# ANIME STORAGE SERVICES
##############################################################


def get_animes(**kwargs) -> list[Anime]:
    return [
        Anime.from_model(anime_model)
        for anime_model in repository.get_animes_models(**kwargs)
    ]


# MANGA STORAGE SERVICES
##############################################################


def get_mangas(**kwargs) -> list[Manga]:
    return [
        Manga.from_model(manga_model)
        for manga_model in repository.get_mangas_models(**kwargs)
    ]


# WATCHLIST STORAGE SERVICES
##############################################################


def get_watchlist(name: str) -> Watchlist:
    return Watchlist.from_model(repository.get_watchlist_model(name=name))


def get_watchlists() -> list[Watchlist]:
    return [
        Watchlist.from_model(watchlist_model)
        for watchlist_model in repository.get_watchlists_models()
    ]


def rename_watchlist(prev_name: str, new_name: str):
    watchlist_model = repository.get_watchlist_model(prev_name)
    repository.set_watchlist_model_name(watchlist_model, new_name)


def save_watchlist(watchlist: Watchlist):
    try:
        watchlist_model = repository.get_watchlist_model(watchlist.name)
        repository.set_watchlist_model_medias(
            watchlist_model,
            [repository.get_or_create_media_model(media) for media in watchlist.medias],
        )
    except WatchlistNotFoundError:
        watchlist_model = repository.create_watchlist_model(watchlist)


"""
def add_media_to_watchlist(watchlist: Watchlist, media: Media) -> Watchlist:
    watchlist_model = repository.get_watchlist_model(watchlist.name)
    media_model = repository.get_media_model(media.mal_id, media.type())
    repository.add_media_model_to_watchlist_model(watchlist_model, media_model)
    return Watchlist.from_model(watchlist_model)


def remove_media_from_watchlist(watchlist: Watchlist, media: Media) -> Watchlist:
    watchlist_model = repository.get_watchlist_model(watchlist.name)
    media_model = repository.get_media_model(media.mal_id, media.type())
    repository.remove_media_model_from_watchlist_model(watchlist_model, media_model)
    return Watchlist.from_model(watchlist_model)
"""


def delete_watchlist(name: str):
    watchlist_model = repository.get_watchlist_model(name)
    repository.delete_watchlist_model(watchlist_model)
