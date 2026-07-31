from django.db import IntegrityError

from ...domain.anime import Anime
from ...domain.manga import Manga
from ...domain.media import Demographic, Genre, Media, Theme
from ...domain.watchlist import Watchlist
from ...enums import MediaCompletion
from ...models.repository import repository
from ...utils import TYPE_TO_CLASS

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


def get_media(mal_id: int, media_type: str) -> Media:
    media_cls = TYPE_TO_CLASS[media_type]
    return media_cls.from_model(
        repository.get_media_model(mal_id=mal_id, media_type=media_type)
    )


def get_medias(**kwargs) -> list[Media]:
    medias_models = repository.get_medias_models(**kwargs)
    return [
        get_media(media_model.mal_id, media_model.type())
        for media_model in medias_models
    ]


def create_media(media: Media) -> Media:
    pass
    """
    media_model_cls: AnimeModel | MangaModel = DOMAIN_TO_MODEL[type(media)]
    valid_fields = [
        "mal_id",
        "title",
        "small_image_url",
        "image_url",
        "large_image_url",
        "user_score",
        "format",
        "score",
        "synopsis",
        "number_sections",
        "rank",
        "status",
        "user_score",
        "user_completion",
        "user_current_section",
        "chapters",
        "rating",
    ]
    data = {
        field: value for field, value in media.__dict__.items() if field in valid_fields
    }
    repository.create_media_model(media)
    media_model = media_model_cls.objects.create(**data)
    media_model.user_completion = media.user_completion.value

    repository._set_media_model_themes(media_model, media.themes)
    repository._set_media_model_genres(media_model, media.genres)
    repository._set_media_model_demographics(media_model, media.demographics)
    if media.type == "anime":
        repository._set_manga_model_authors(media_model, media.authors)
    else:
        repository._set_anime_model_studios(media_model, media.studios)

    
    media_model.relations.all().delete()
    if not media.relations is None:
        for relation in media.relations:
            media_model.relations.create(
                origin_media=media_model, relation_type=relation.type
            )
    
    return media
    """


def update_media(media: Media):
    media_model = repository.get_media_model(media.mal_id, media.type())
    media_model.user_completion = media.user_completion
    media_model.user_score = media.user_score
    media_model.user_current_section = media.user_current_section
    try:
        media_model.save()
        return TYPE_TO_CLASS[media.type()].from_model(media_model)

    except IntegrityError:
        raise ValueError(
            f"Mise à jour des données utilisateurs du média {media.mal_id} impossible."
        )


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


def update_media_user_completion(
    mal_id: int,
    media_type: str,
):
    media_model = repository.get_media_model(mal_id=mal_id, media_type=media_type)
    return repository._update_media_model_user_completion(media_model)


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


def set_watchlist_name(prev_name: str, new_name: str):
    watchlist_model = repository.get_watchlist_model(prev_name)
    try:
        watchlist_model.name = new_name
        watchlist_model.save()
    except IntegrityError:
        raise ValueError(
            f"Impossible de modifier le nom de la watchlist {prev_name} pour {new_name}"
        )


def create_watchlist(watchlist: Watchlist) -> Watchlist:
    repository.create_watchlist_model(watchlist)
    return watchlist


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


def delete_watchlist(name: str):
    watchlist_model = repository.get_watchlist_model(name)
    repository.delete_watchlist_model(watchlist_model)
