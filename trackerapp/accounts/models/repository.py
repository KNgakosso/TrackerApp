from ...exceptions import MediaNotFoundError
from ...tracking.models.media_models import MediaModel
from ..enums import MediaCompletion
from .media_user_infos_model import MediaUserInfosModel


def get_media_user_infos_model(user, media_model: MediaModel) -> MediaUserInfosModel:
    try:
        return MediaUserInfosModel.objects.get(user=user, media=media_model)
    except MediaUserInfosModel.DoesNotExist as exc:
        raise MediaNotFoundError(
            f"No media infos found for user {user} id : {media_model.mal_id}."
        ) from exc


def set_media_user_infos_model_user_completion(
    media_user_infos_model: MediaUserInfosModel, new_completion: MediaCompletion
) -> MediaCompletion:
    media_user_infos_model.completion = new_completion
    media_user_infos_model.save()
    return media_user_infos_model.completion


def set_media_user_infos_model_user_current_section(
    media_user_infos_model: MediaUserInfosModel, new_current_section: int | None
) -> int | None:
    media_user_infos_model.current_section = new_current_section
    media_user_infos_model.save()
    return media_user_infos_model.current_section


def set_media_user_infos_model_user_score(
    media_user_infos_model: MediaUserInfosModel, new_score: int | None
) -> int | None:
    try:
        media_user_infos_model.score = new_score
        media_user_infos_model.save()
        return media_user_infos_model.score
    except IntegrityError as exc:
        raise InvalidScoreError(
            "Score must be an integer between 0 and 10, or None."
        ) from exc
