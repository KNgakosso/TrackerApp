from itertools import chain

from django.core.exceptions import FieldError
from django.db import IntegrityError

from ...domain.media import Media
from ...domain.watchlist import Watchlist
from ...enums import MediaCompletion, MediaType
from ...utils import TYPE_TO_MODEL
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


def _set_media_model_genres(media_model: MediaModel, genres: list[GenreModel]):
    media_model.genres.set(genres)
    media_model.save()


# THEME MODEL
#########################################


def get_theme_model(name: str) -> ThemeModel:
    try:
        return ThemeModel.objects.get(name=name)
    except ThemeModel.DoesNotExist:
        raise ValueError(f"Aucun thème trouvé au nom de {name}.")


def _set_media_model_themes(media_model: MediaModel, themes: list[ThemeModel]):
    media_model.themes.set(themes)
    media_model.save()


# DEMOGRAPHIC MODEL
#########################################


def get_demographic_model(name: str) -> DemographicModel:
    try:
        return DemographicModel.objects.get(name=name)
    except DemographicModel.DoesNotExist:
        raise ValueError(f"Aucune démographie trouvée au nom de {name}.")


def _set_media_model_demographics(
    media_model: MediaModel, demographics: list[DemographicModel]
):
    media_model.demographics.set(demographics)
    media_model.save()


# MEDIA MODEL
#########################################


def create_media_model(media: Media) -> MediaModel:
    media_model_cls = TYPE_TO_MODEL[media.media_type]
    valid_fields = [
        "themes",
        "demographics",
        "genres",
        "authors",
        "studios",
        "images_urls",
    ]
    data = {
        field: value
        for field, value in media.__dict__.items()
        if not field in valid_fields
    }

    data["small_image_url"] = (
        media.images_urls.small_image_url if media.images_urls else ""
    )
    data["image_url"] = media.images_urls.image_url if media.images_urls else ""
    data["large_image_url"] = (
        media.images_urls.large_image_url if media.images_urls else ""
    )

    media_model = media_model_cls.objects.create(**data)
    _set_media_model_themes(
        media_model, [get_theme_model(theme.name) for theme in media.themes]
    )
    _set_media_model_genres(
        media_model, [get_genre_model(genre.name) for genre in media.genres]
    )
    _set_media_model_demographics(
        media_model,
        [get_demographic_model(demographic.name) for demographic in media.demographics],
    )
    if isinstance(media_model, MangaModel):
        _set_manga_model_authors(
            media_model, [get_author_model(author.mal_id) for author in media.authors]
        )
    elif isinstance(media_model, AnimeModel):
        _set_anime_model_studios(
            media_model, [get_studio_model(studio.mal_id) for studio in media.studios]
        )
    return get_media_model(media.mal_id, media.media_type)


def get_media_model(mal_id: int, media_type: MediaType) -> MediaModel:
    try:
        media_model = MediaModel.objects.instance_of(TYPE_TO_MODEL[media_type]).get(
            mal_id=mal_id
        )
        return media_model
    except MediaModel.DoesNotExist:
        raise ValueError(f"Aucun {media_type} trouvé pour l'id {mal_id}.")


def get_or_create_media_model(media: Media) -> MediaModel:
    try:
        return get_media_model(media.mal_id, media.media_type)
    except ValueError:
        return create_media_model(media)


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
    except (AnimeModel.DoesNotExist, ValueError):
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


def _set_anime_model_studios(anime_model: AnimeModel, studios: list[StudioModel]):
    anime_model.studios.set(studios)
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


def _set_manga_model_authors(manga_model: MangaModel, authors: list[AuthorModel]):
    manga_model.authors.set(authors)
    manga_model.save()


# WATCHLIST MODEL
#########################################


def get_watchlist_model(name: str) -> WatchlistModel:
    try:
        return WatchlistModel.objects.get(name=name)
    except WatchlistModel.DoesNotExist:
        raise ValueError(f"Aucune Watchlist trouvée au nom de {name}")


def get_watchlists_models(**kwargs) -> list[WatchlistModel]:
    return list(WatchlistModel.objects.filter(**kwargs))


def create_watchlist_model(watchlist: Watchlist) -> WatchlistModel:
    try:
        data = {
            field: value
            for field, value in watchlist.__dict__.items()
            if field != "medias"
        }
        watchlist_model = WatchlistModel.objects.create(**data)
        set_watchlist_model_medias(
            watchlist_model,
            [
                get_media_model(media.mal_id, media.media_type)
                for media in watchlist.medias
            ],
        )
        return get_watchlist_model(watchlist.name)
    except IntegrityError:
        raise ValueError("Erreur lors de l'enregistrement de la watchlist.")


def set_watchlist_model_medias(
    watchlist_model: WatchlistModel, medias: list[MediaModel]
):
    watchlist_model.medias.set(medias)
    watchlist_model.save()


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
