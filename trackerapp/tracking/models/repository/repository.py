from itertools import chain
from typing import Any

from django.core.exceptions import FieldError
from django.db import IntegrityError

from ...domain.anime import Studio
from ...domain.manga import Author
from ...domain.media import Media
from ...domain.watchlist import Watchlist
from ...enums import MediaCompletion, MediaType
from ...exceptions import (
    InvalidScoreError,
    MediaError,
    MediaNotFoundError,
    NotFoundError,
    StorageError,
    WatchlistError,
    WatchlistNotFoundError,
)
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
        raise NotFoundError(f"No genre named '{name}' found.")


def _set_media_model_genres(media_model: MediaModel, genres: list[GenreModel]):
    media_model.genres.set(genres)
    media_model.save()


# THEME MODEL
#########################################


def get_theme_model(name: str) -> ThemeModel:
    try:
        return ThemeModel.objects.get(name=name)
    except ThemeModel.DoesNotExist:
        raise NotFoundError(f"No theme named '{name}' found.")


def _set_media_model_themes(media_model: MediaModel, themes: list[ThemeModel]):
    media_model.themes.set(themes)
    media_model.save()


# DEMOGRAPHIC MODEL
#########################################


def get_demographic_model(name: str) -> DemographicModel:
    try:
        return DemographicModel.objects.get(name=name)
    except DemographicModel.DoesNotExist:
        raise NotFoundError(f"No demographic named '{name}' found.")


def _set_media_model_demographics(
    media_model: MediaModel, demographics: list[DemographicModel]
):
    media_model.demographics.set(demographics)
    media_model.save()


# MEDIA MODEL
#########################################
def _prepare_data(media: Media) -> dict[str, Any]:
    many_to_many_fields = [
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
        if not field in many_to_many_fields
    }

    data["small_image_url"] = (
        media.images_urls.small_image_url if media.images_urls else ""
    )
    data["image_url"] = media.images_urls.image_url if media.images_urls else ""
    data["large_image_url"] = (
        media.images_urls.large_image_url if media.images_urls else ""
    )
    data["title_english"] = media.title_english or ""
    data["title_french"] = media.title_french or ""
    data["format"] = media.format or ""
    data["synopsis"] = media.synopsis or ""
    data["synopsis_translated"] = media.synopsis_translated or ""
    return data


def create_media_model(media: Media) -> MediaModel:
    try:
        media_model_cls = TYPE_TO_MODEL[media.media_type]
        data = _prepare_data(media)
        media_model = media_model_cls.objects.create(**data)
        _set_media_model_themes(
            media_model, [get_theme_model(theme.name) for theme in media.themes]
        )
        _set_media_model_genres(
            media_model, [get_genre_model(genre.name) for genre in media.genres]
        )
        _set_media_model_demographics(
            media_model,
            [
                get_demographic_model(demographic.name)
                for demographic in media.demographics
            ],
        )
        if isinstance(media_model, MangaModel):
            _set_manga_model_authors(
                media_model,
                [get_or_create_author_model(author) for author in media.authors],
            )
        elif isinstance(media_model, AnimeModel):
            _set_anime_model_studios(
                media_model,
                [get_or_create_studio_model(studio) for studio in media.studios],
            )
        return get_media_model(media.mal_id, media.media_type)
    except IntegrityError as exc:
        raise StorageError(
            f"Error during the creation of media id : {media.mal_id}"
        ) from exc


def media_model_exists(mal_id: int, media_type: MediaType) -> bool:
    return (
        MediaModel.objects.instance_of(TYPE_TO_MODEL[media_type])
        .filter(mal_id=mal_id)
        .exists()
    )


def get_media_model(mal_id: int, media_type: MediaType) -> MediaModel:
    try:
        media_model = MediaModel.objects.instance_of(TYPE_TO_MODEL[media_type]).get(
            mal_id=mal_id
        )
        return media_model
    except MediaModel.DoesNotExist as exc:
        raise MediaNotFoundError(f"No {media_type} found with id : {mal_id}.") from exc


def get_or_create_media_model(media: Media) -> MediaModel:
    try:
        return get_media_model(media.mal_id, media.media_type)
    except MediaNotFoundError:
        return create_media_model(media)


def get_medias_models(**kwargs) -> list[MediaModel]:
    try:
        anime_queryset = MediaModel.objects.instance_of(AnimeModel).filter(**kwargs)
        manga_queryset = MediaModel.objects.instance_of(MangaModel).filter(**kwargs)
        return list(chain(anime_queryset, manga_queryset))
    except FieldError as exc:
        raise MediaError(f"Invalid filters : {exc}.") from exc


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
        raise InvalidScoreError(
            "Score must be an integer between 0 and 10, or None."
        ) from exc


def set_media_model_synopsis_tanslated(
    media_model: MediaModel, synopsis_translated: str
) -> str:
    media_model.synopsis_translated = synopsis_translated
    media_model.save()
    return media_model.synopsis_translated


# EPISODE MODEL
#########################################


def get_episode_model(anime_mal_id: int, episode_mal_id: int) -> EpisodeModel:
    try:
        return EpisodeModel.objects.get(
            anime_mal_id=anime_mal_id, episode_mal_id=episode_mal_id
        )
    except EpisodeModel.DoesNotExist as exc:
        raise NotFoundError(
            f"No episode found with id : {episode_mal_id}, anime_id : {anime_mal_id}."
        ) from exc


# ANIME MODEL
#########################################


def get_anime_model(mal_id: int) -> AnimeModel:
    try:
        return AnimeModel.objects.get(mal_id=mal_id)
    except AnimeModel.DoesNotExist as exc:
        raise NotFoundError(f"No anime found with id : {mal_id}.") from exc


def get_animes_models(**kwargs) -> list[AnimeModel]:
    try:
        anime_queryset = AnimeModel.objects.instance_of(AnimeModel).filter(**kwargs)
        return list(anime_queryset)
    except FieldError as exc:
        raise MediaError(f"Invalid filters : {exc}") from exc


def get_studio_model(mal_id: int) -> StudioModel:
    try:
        return StudioModel.objects.get(mal_id=mal_id)
    except StudioModel.DoesNotExist as exc:
        raise NotFoundError(f"No studio found with id : {mal_id}.") from exc


def create_studio(studio: Studio) -> StudioModel:
    try:
        return StudioModel.objects.create(mal_id=studio.mal_id, name=studio.name)
    except IntegrityError as exc:
        raise StorageError(f"Error during creation of studio {studio.mal_id}") from exc


def get_or_create_studio_model(studio: Studio) -> StudioModel:
    try:
        return get_studio_model(studio.mal_id)
    except NotFoundError:
        return create_studio(studio)


def _set_anime_model_studios(anime_model: AnimeModel, studios: list[StudioModel]):
    anime_model.studios.set(studios)
    anime_model.save()


# MANGA MODEL
#########################################


def get_manga_model(mal_id: int) -> MangaModel:
    try:
        return MangaModel.objects.get(mal_id=mal_id)
    except MangaModel.DoesNotExist as exc:
        raise NotFoundError(f"No manga found with id : {mal_id}.") from exc


def get_mangas_models(**kwargs) -> list[MangaModel]:
    try:
        manga_queryset = MediaModel.objects.instance_of(MangaModel).filter(**kwargs)
        return list(manga_queryset)
    except FieldError as exc:
        raise MediaError(f"Invalid filters : {exc}") from exc


def get_author_model(mal_id: int) -> AuthorModel:
    try:
        return AuthorModel.objects.get(mal_id=mal_id)
    except AuthorModel.DoesNotExist as exc:
        raise NotFoundError(f"No author found with id : {mal_id}.") from exc


def create_author(author: Author) -> AuthorModel:
    try:
        return AuthorModel.objects.create(mal_id=author.mal_id, name=author.name)
    except IntegrityError as exc:
        raise StorageError(f"Error during creation of author {author.mal_id}") from exc


def get_or_create_author_model(author: Author) -> AuthorModel:
    try:
        return get_author_model(author.mal_id)
    except NotFoundError:
        return create_author(author)


def _set_manga_model_authors(manga_model: MangaModel, authors: list[AuthorModel]):
    manga_model.authors.set(authors)
    manga_model.save()


# WATCHLIST MODEL
#########################################


def get_watchlist_model(name: str) -> WatchlistModel:
    try:
        return WatchlistModel.objects.get(name=name)
    except WatchlistModel.DoesNotExist as exc:
        raise WatchlistNotFoundError(f"No watchlist named {name} found.") from exc


def get_watchlists_models(**kwargs) -> list[WatchlistModel]:
    try:
        return list(WatchlistModel.objects.filter(**kwargs))
    except FieldError as exc:
        raise WatchlistError(f"Invalid filters : {exc}") from exc


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
