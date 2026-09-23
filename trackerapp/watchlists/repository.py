from medias.models.media_models import MediaModel

from .exceptions import WatchlistError, WatchlistNotFoundError
from .models import WatchlistModel

# WATCHLIST MODEL
#########################################


def get_watchlist_model(user, name: str) -> WatchlistModel:
    try:
        return WatchlistModel.objects.get(user=user, name=name)
    except WatchlistModel.DoesNotExist as exc:
        raise WatchlistNotFoundError(
            f"User {user} has no watchlist named {name} found."
        ) from exc


def get_watchlists_models(user, **kwargs) -> list[WatchlistModel]:
    try:
        return list(WatchlistModel.objects.filter(user=user, **kwargs))
    except FieldError as exc:
        raise WatchlistError(f"Invalid filters : {exc}") from exc


def create_watchlist_model(user, watchlist: Watchlist) -> WatchlistModel:
    try:
        data = {
            field: value
            for field, value in watchlist.__dict__.items()
            if field != "medias"
        }
        data["user"] = user
        watchlist_model = WatchlistModel.objects.create(**data)
        set_watchlist_model_medias(
            watchlist_model,
            [
                get_media_model(media.mal_id, media.media_type)
                for media in watchlist.medias
            ],
        )
        return get_watchlist_model(user, watchlist.name)
    except IntegrityError as exc:
        raise StorageError(
            f"Error during the creation of watchlist {watchlist.name}."
        ) from exc


def set_watchlist_model_medias(
    watchlist_model: WatchlistModel, medias: list[MediaModel]
):
    watchlist_model.medias.set(medias)
    watchlist_model.save()


def set_watchlist_model_name(watchlist_model: WatchlistModel, new_name: str):
    try:
        watchlist_model.name = new_name
        watchlist_model.save()
    except IntegrityError as exc:
        raise StorageError(
            f"Impossible to rename the watchlist into {new_name}."
        ) from exc


def add_media_model_to_watchlist_model(
    watchlist_model: WatchlistModel, media_model: MediaModel
):
    watchlist_model.medias.add(media_model)
    watchlist_model.save()


def remove_media_model_from_watchlist_model(
    watchlist_model: WatchlistModel, media_model: MediaModel
):
    watchlist_model.medias.remove(media_model)
    watchlist_model.save()


def delete_watchlist_model(watchlist_model: WatchlistModel):
    watchlist_model.delete()
