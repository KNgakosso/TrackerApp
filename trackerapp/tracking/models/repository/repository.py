from itertools import chain

from django.core.exceptions import FieldError
from django.db import IntegrityError

from ...domain.anime import Studio
from ...domain.manga import Author
from ...domain.media import Demographic, Genre, Media, Theme
from ...domain.watchlist import Watchlist
from ...enums import MediaCompletion
from ...utils import DOMAIN_TO_MODEL, TYPE_TO_MODEL
from ..anime_models import AnimeModel, EpisodeModel, StudioModel
from ..manga_models import AuthorModel, MangaModel
from ..media_models import DemographicModel, GenreModel, MediaModel, ThemeModel
from ..watchlist_model import WatchlistModel

# GENRE MODEL
#########################################


def get_genre_model(name: str) -> GenreModel:
    try:
        return GenreModel.objects.get(name=name)
    except GenreModel.DoesNotExist:
        raise ValueError(f"Aucun genre trouvé au nom de {name}.")


def _set_media_model_genres(media_model: MediaModel, genres: list[Genre]):
    media_model.genres.set([get_genre_model(genre.name) for genre in genres])
    media_model.save()


# THEME MODEL
#########################################


def get_theme_model(name: str) -> ThemeModel:
    try:
        return ThemeModel.objects.get(name=name)
    except ThemeModel.DoesNotExist:
        raise ValueError(f"Aucun thème trouvé au nom de {name}.")


def _set_media_model_themes(media_model: MediaModel, themes: list[Theme]):
    media_model.themes.set([get_theme_model(theme.name) for theme in themes])
    media_model.save()


# DEMOGRAPHIC MODEL
#########################################


def get_demographic_model(name: str) -> DemographicModel:
    try:
        return DemographicModel.objects.get(name=name)
    except DemographicModel.DoesNotExist:
        raise ValueError(f"Aucune démographie trouvée au nom de {name}.")


def _set_media_model_demographics(
    media_model: MediaModel, demographics: list[Demographic]
):
    media_model.demographics.set(
        [get_demographic_model(demographic.name) for demographic in demographics]
    )
    media_model.save()


# MEDIA MODEL
#########################################


def create_media_model(media: Media) -> MediaModel:
    media_model_cls: AnimeModel | MangaModel = DOMAIN_TO_MODEL[type(media)]
    valid_fields = ["themes", "demographics", "genres", "authors", "studios"]
    data = {
        field: value
        for field, value in media.__dict__.items()
        if not field in valid_fields
    }
    media_model = media_model_cls.objects.create(**data)
    # media_model.user_completion = media.user_completion.value
    _set_media_model_themes(media_model, media.themes)
    _set_media_model_genres(media_model, media.genres)
    _set_media_model_demographics(media_model, media.demographics)
    if isinstance(media_model, MangaModel):
        _set_manga_model_authors(media_model, media.authors)
    elif isinstance(media_model, AnimeModel):
        _set_anime_model_studios(media_model, media.studios)
    return media_model


def get_media_model(mal_id: int, media_type: str) -> MediaModel:
    try:
        media_model = MediaModel.objects.instance_of(TYPE_TO_MODEL[media_type]).get(
            mal_id=mal_id
        )
        return media_model
    except MediaModel.DoesNotExist:
        raise ValueError(f"Aucun {media_type} trouvé pour l'id {mal_id}.")


def get_medias_models(**kwargs) -> list[MediaModel]:
    try:
        anime_queryset = MediaModel.objects.instance_of(AnimeModel).filter(**kwargs)
        manga_queryset = MediaModel.objects.instance_of(MangaModel).filter(**kwargs)
        return list(chain(anime_queryset, manga_queryset))
    except FieldError as e:
        raise ValueError(f"Filtres de recherche invalides : {e}") from e


def set_media_model_user_completion(
    media_model: MediaModel, new_completion: MediaCompletion
) -> MediaCompletion:
    media_model.user_completion = new_completion
    media_model.save()
    return media_model.user_completion


def set_media_model_user_current_section(
    media_model: MediaModel, new_current_section: int | None
) -> int | None:
    media_model.user_current_section = new_current_section
    media_model.save()
    return media_model.user_current_section


def set_media_model_user_score(
    media_model: MediaModel, new_score: int | None
) -> int | None:
    try:
        media_model.user_score = new_score
        media_model.save()
        return media_model.user_score
    except IntegrityError as exc:
        raise ValueError(
            "Le Score doit être un entier entre 0 et 10, ou la valeur None."
        ) from exc


# EPISODE MODEL
#########################################


def get_episode_model(anime_mal_id: int, episode_mal_id: int) -> EpisodeModel:
    try:
        return EpisodeModel.objects.get(
            anime_mal_id=anime_mal_id, episode_mal_id=episode_mal_id
        )
    except EpisodeModel.DoesNotExist:
        raise ValueError


# ANIME MODEL
#########################################


def get_anime_model(mal_id: int) -> AnimeModel:
    try:
        return AnimeModel.objects.get(mal_id=mal_id)
    except AnimeModel.DoesNotExist:
        raise ValueError(f"Aucun animé trouvé pour l'id {mal_id}")


def get_animes_models(**kwargs) -> list[AnimeModel]:
    try:
        anime_queryset = AnimeModel.objects.instance_of(AnimeModel).filter(**kwargs)
        return list(anime_queryset)
    except FieldError as e:
        raise ValueError(f"Filtres de recherche invalides : {e}") from e


def get_studio_model(mal_id: int) -> StudioModel:
    try:
        return StudioModel.objects.get(mal_id=mal_id)
    except StudioModel.DoesNotExist:
        raise ValueError(f"Aucun studio trouvé pour mal_id : {mal_id}.")


def _set_anime_model_studios(anime_model: AnimeModel, studios: list[Studio]):
    anime_model.studios.set([get_studio_model(studio.mal_id) for studio in studios])
    anime_model.save()


# MANGA MODEL
#########################################


def get_manga_model(mal_id: int) -> MangaModel:
    try:
        return MangaModel.objects.get(mal_id=mal_id)
    except MangaModel.DoesNotExist:
        raise ValueError(f"Aucun manga trouvé pour l'id {mal_id}")


def get_mangas_models(**kwargs) -> list[MangaModel]:
    try:
        manga_queryset = MediaModel.objects.instance_of(MangaModel).filter(**kwargs)
        return list(manga_queryset)
    except FieldError as e:
        raise ValueError(f"Filtres de recherche invalides : {e}") from e


def get_author_model(mal_id: int) -> AuthorModel:
    try:
        return AuthorModel.objects.get(mal_id=mal_id)
    except AuthorModel.DoesNotExist:
        raise ValueError(f"Aucun auteur trouvé pour mal_id : {mal_id}.")


def _set_manga_model_authors(manga_model: MangaModel, authors: list[Author]):
    manga_model.authors.set([get_author_model(author.mal_id) for author in authors])
    manga_model.save()


# WATCHLIST MODEL
#########################################


def get_watchlist_model(name: str) -> WatchlistModel:
    try:
        return WatchlistModel.objects.get(name=name)
    except WatchlistModel.DoesNotExist:
        raise ValueError(f"Aucune Watchlist trouvée au nom de {name}")


def get_watchlists_models() -> list[WatchlistModel]:
    return list(WatchlistModel.objects.all())


def create_watchlist_model(watchlist: Watchlist) -> WatchlistModel:
    try:
        data = {
            field: value
            for field, value in watchlist.__dict__.items()
            if field != "medias"
        }
        return WatchlistModel.objects.create(**data)
    except IntegrityError:
        raise ValueError("Erreur lors de l'enregistrement de la watchlist.")


def add_media_model_to_watchlist_model(
    watchlist_model: WatchlistModel, media_model: MediaModel
):
    # Empêcher l'ajout 2 fois
    watchlist_model.medias.add(media_model)
    watchlist_model.save()


def remove_media_model_from_watchlist_model(
    watchlist_model: WatchlistModel, media_model: MediaModel
):
    # Intercepter les erreurs
    watchlist_model.medias.remove(media_model)
    watchlist_model.save()


def delete_watchlist_model(watchlist_model: WatchlistModel):
    try:
        watchlist_model.delete()
    except WatchlistModel.DoesNotExist:
        raise ValueError(
            f"Erreur lors de la suppression de la watchlist {watchlist_model.name}"
        )
