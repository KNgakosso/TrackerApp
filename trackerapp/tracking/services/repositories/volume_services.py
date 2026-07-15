from ...models.manga_models import VolumeModel

def _get_volume_model(manga_mal_id : int, volume_mal_id : int) -> VolumeModel:
    try:
        return VolumeModel.objects.get(manga_mal_id=manga_mal_id, volume_mal_id=volume_mal_id)
    except VolumeModel.DoesNotExist:
        raise ValueError

def set_volume_user_score(manga_mal_id : int, volume_mal_id : int, new_user_score = float):
    volume_model = _get_volume_model(manga_mal_id, volume_mal_id)
    volume_model.user_score = new_user_score

def set_volume_user_completion(manga_mal_id : int, volume_mal_id : int, new_user_completion = str):
    volume_model = _get_volume_model(manga_mal_id, volume_mal_id)
    volume_model.user_score = new_user_completion