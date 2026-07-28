from itertools import chain

from django.core.exceptions import FieldError
from django.db import IntegrityError

from ...domain.enums import MediaCompletion
from ...domain.media import Demographic, Genre, Media, Theme
from ...models import AnimeModel, MangaModel
from ...models.media_models import DemographicModel, GenreModel, MediaModel, ThemeModel
from ..utils import DOMAIN_TO_MODEL, TYPE_TO_CLASS, TYPE_TO_MODEL


def _get_genre_model(name: str) -> GenreModel:
    try:
        return GenreModel.objects.get(name=name)
    except GenreModel.DoesNotExist:
        raise ValueError(f"Aucun genre trouvé au nom de {name}.")


def _get_theme_model(name: str) -> ThemeModel:
    try:
        return ThemeModel.objects.get(name=name)
    except ThemeModel.DoesNotExist:
        raise ValueError(f"Aucun thème trouvé au nom de {name}.")


def _get_demographic_model(name: str) -> DemographicModel:
    try:
        return DemographicModel.objects.get(name=name)
    except DemographicModel.DoesNotExist:
        raise ValueError(f"Aucune démographie trouvée au nom de {name}.")


def _get_media_model(mal_id: int, media_type: str) -> MediaModel:
    try:
        media_model = MediaModel.objects.instance_of(TYPE_TO_MODEL[media_type]).get(
            mal_id=mal_id
        )
        return media_model
    except MediaModel.DoesNotExist:
        raise ValueError(f"Aucun {media_type} trouvé pour l'id {mal_id}.")


def _get_medias_models(**kwargs) -> list[MediaModel]:
    try:
        anime_queryset = MediaModel.objects.instance_of(AnimeModel).filter(**kwargs)
        manga_queryset = MediaModel.objects.instance_of(MangaModel).filter(**kwargs)
        return list(chain(anime_queryset, manga_queryset))
    except FieldError as e:
        raise ValueError(f"Filtres de recherche invalides : {e}") from e


def _set_media_model_user_completion(
    media_model: MediaModel, new_completion: MediaCompletion
) -> MediaCompletion:
    media_model.user_completion = new_completion
    media_model.save()
    return media_model.user_completion


def _set_media_model_user_current_section(
    media_model: MediaModel, new_current_section: int | None
) -> int | None:
    media_model.user_current_section = new_current_section
    media_model.save()
    return media_model.user_current_section


def _set_media_model_user_score(
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


"""
def _set_media_user_current_section(media_model: MediaModel, new_current_section: int):
    if new_current_section > media_model.number_sections:
        raise ValueError(
            "Le numéro de la section ne peut pas être au dessus du nombre de sections"
        )
    try:
        media_model.user_current_section = new_current_section
        media_model.save()
        return media_model.user_current_section
    except IntegrityError:
        raise ValueError("Une erreur d'intégrite est survenue lors de l'enregistrement")

"""


def _update_media_model_user_completion(media_model: MediaModel):
    if media_model.number_sections is None:
        raise ValueError(
            "Impossible de mettre à jour la complétion sans valeur de number_sections."
        )
    if media_model.user_current_section == media_model.number_sections:
        completion = MediaCompletion.COMPLETED
    elif media_model.user_current_section == 0:
        completion = MediaCompletion.NOT_STARTED
    elif (
        media_model.user_current_section > 0
        and media_model.user_current_section < media_model.number_sections
    ):
        completion = MediaCompletion.IN_PROGRESS
    return _set_media_model_user_completion(media_model, completion)


def get_media(mal_id: int, media_type: str) -> Media:
    media_cls = TYPE_TO_CLASS[media_type]
    return media_cls.from_model(_get_media_model(mal_id=mal_id, media_type=media_type))


def get_medias(**kwargs) -> list[Media]:
    medias_models = _get_medias_models(**kwargs)
    return [
        get_media(media_model.mal_id, media_model.type())
        for media_model in medias_models
    ]


def get_genre(name: str) -> Genre:
    return Genre.from_model(_get_genre_model(name=name))


def get_demographic(name: str) -> Demographic:
    return Demographic.from_model(_get_demographic_model(name=name))


def get_theme(name: str) -> Theme:
    return Theme.from_model(_get_theme_model(name=name))


def create_media(media: Media) -> Media:
    media_model_cls: AnimeModel | MangaModel = DOMAIN_TO_MODEL[type(media)]
    valid_fields = [
        "mal_id",
        "title",
        "user_score",
        # "user_completion",
        "score",
        "rank",
        "status",
        "user_current_episode",
        "rating",
        "number_episodes",
        "number_seasons",
        "user_current_section",
        "number_sections",
        "user_current_volume",
        "number_volumes",
        "user_current_section",
    ]
    data = {
        field: value for field, value in media.__dict__.items() if field in valid_fields
    }
    media_model = media_model_cls.objects.create(**data)
    media_model.user_completion = media.user_completion.value

    media_model.themes.set([_get_theme_model(theme.name) for theme in media.themes])
    media_model.genres.set([_get_genre_model(genre.name) for genre in media.genres])
    media_model.demographics.set(
        [_get_demographic_model(demographic.name) for demographic in media.demographics]
    )

    """
    media_model.relations.all().delete()
    if not media.relations is None:
        for relation in media.relations:
            media_model.relations.create(
                origin_media=media_model,
                relation_type = relation.type
            )
    """
    media_model.save()
    images = ImagesModel.objects.create(
        media=media_model,
        small_image_url=media.images.webp.small_image_url,
        medium_image_url=media.images.webp.medium_image_url,
        large_image_url=media.images.webp.large_image_url,
    )
    images.save()
    return media


def update_media(media: Media):
    media_model = _get_media_model(media.mal_id, media.type())
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


def set_media_user_completion(mal_id: int, media_type: str, new_completion: str) -> str:
    media_model = _get_media_model(mal_id=mal_id, media_type=media_type)
    return _set_media_model_user_completion(media_model, new_completion)


def set_media_user_current_section(
    mal_id: int, media_type: str, new_current_section: int
):
    media_model = _get_media_model(mal_id=mal_id, media_type=media_type)
    return _set_media_user_current_section(media_model, new_current_section)


def update_media_user_completion(
    mal_id: int,
    media_type: str,
):
    media_model = _get_media_model(mal_id=mal_id, media_type=media_type)
    return _update_media_model_user_completion(media_model)
