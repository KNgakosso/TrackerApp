from ...models.watchlist_model import WatchlistModel
from ...domain.watchlist import Watchlist
from ...domain.media import Media
from ..repositories import media_services
from django.db import IntegrityError

def _get_watchlist_model(name : str) -> WatchlistModel:
    try:
        return WatchlistModel.objects.get(name=name)
    except WatchlistModel.DoesNotExist:
        raise ValueError(f"Aucune Watchlist trouvée au nom de {name}")

def get_watchlist(name : str) -> Watchlist:
    return Watchlist.from_model(_get_watchlist_model(name=name))

def get_watchlists() -> list[Watchlist]:
    queryset = WatchlistModel.objects.all()
    return [Watchlist.from_model(watchlist_model) for watchlist_model in queryset]

def set_watchlist_name(prev_name : str, new_name : str):
    watchlist_model = _get_watchlist_model(prev_name)
    try:
        watchlist_model.name = new_name
        watchlist_model.save()
    except IntegrityError:
        raise ValueError(f"Impossible de modofier le nom de la watchlist {prev_name} pour {new_name}")
    
def create_watchlist_model(watchlist : Watchlist) -> WatchlistModel:
    try:
        data = {
        field : value
        for field,value in watchlist.__dict__.items()
        if not field == "medias"
        }
        return WatchlistModel.objects.create(**data)
    except IntegrityError:
        raise ValueError("Erreur lors de l'enregistrement de la watchlist.")

def add_media_to_watchlist(watchlist : Watchlist, media : Media) -> Watchlist:
    watchlist_model = _get_watchlist_model(watchlist.name)
    media_model = media_services._get_media_model(media.mal_id, media.type())
    watchlist_model.medias.add(media_model)
    watchlist_model.save()
    return Watchlist.from_model(watchlist_model)

def remove_media_from_watchlist(watchlist : Watchlist, media : Media) -> Watchlist:
    watchlist_model = _get_watchlist_model(watchlist.name)
    media_model = media_services._get_media_model(media.mal_id, media.type())
    watchlist_model.medias.remove(media_model)
    watchlist_model.save()
    return Watchlist.from_model(watchlist_model)

def delete_watchlist(name : str):
    watchlist_model = _get_watchlist_model(name)
    try:
        watchlist_model.delete()
    except WatchlistModel.DoesNotExist:
        raise ValueError(f"Erreur lors de la suppression de la watchlist {name}")
    