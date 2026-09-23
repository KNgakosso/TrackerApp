from . import repository
from .domain import Watchlist
from .exceptions import WatchlistNotFoundError

# WATCHLIST STORAGE SERVICES

##############################################################


def get_watchlist(user, name: str) -> Watchlist:
    return Watchlist.from_model(repository.get_watchlist_model(user=user, name=name))


def get_watchlists(user) -> list[Watchlist]:
    return [
        Watchlist.from_model(watchlist_model)
        for watchlist_model in repository.get_watchlists_models(user=user)
    ]


def rename_watchlist(user, prev_name: str, new_name: str):
    watchlist_model = repository.get_watchlist_model(user, prev_name)
    repository.set_watchlist_model_name(watchlist_model, new_name)


def save_watchlist(user, watchlist: Watchlist):
    try:
        watchlist_model = repository.get_watchlist_model(user, watchlist.name)
        repository.set_watchlist_model_medias(
            watchlist_model,
            [repository.get_or_create_media_model(media) for media in watchlist.medias],
        )
    except WatchlistNotFoundError:
        watchlist_model = repository.create_watchlist_model(user, watchlist)


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


def delete_watchlist(user, name: str):
    watchlist_model = repository.get_watchlist_model(user, name)
    repository.delete_watchlist_model(watchlist_model)
