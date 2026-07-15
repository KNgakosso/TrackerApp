from ...models.anime_models import EpisodeModel
from ...domain.episode import Episode
from .anime_services import _get_anime_model

def _get_episode_model(anime_mal_id : int, episode_mal_id : int) -> EpisodeModel:
    try:
        return EpisodeModel.objects.get(anime_mal_id=anime_mal_id, episode_mal_id=episode_mal_id)
    except EpisodeModel.DoesNotExist:
        raise ValueError
    
def get_episode(anime_mal_id : int, episode_mal_id : int) -> Episode:
    return Episode.from_model(_get_episode_model(anime_mal_id=anime_mal_id, episode_mal_id=episode_mal_id))

def get_episodes(anime_mal_id : int) -> list[Episode]:
    anime_model = _get_anime_model(mal_id=anime_mal_id)
    return [Episode.from_model(episode_model) for episode_model in anime_model.episodes.all()]

def set_episode_user_score(anime_mal_id : int, episode_mal_id : int, new_user_score = float):
    episode_model = _get_episode_model(anime_mal_id, episode_mal_id)
    episode_model.user_score = new_user_score

def set_episode_user_completion(anime_mal_id : int, episode_mal_id : int, new_user_completion = str):
    episode_model = _get_episode_model(anime_mal_id, episode_mal_id)
    episode_model.user_score = new_user_completion