from ...models import AnimeModel
from ...domain.anime import Anime

def _get_anime_model(mal_id : int) -> AnimeModel:
    try:
        return AnimeModel.objects.get(mal_id=mal_id)
    except AnimeModel.DoesNotExist:
        raise ValueError(f"Aucun animé trouvé pour l'id {mal_id}")

def get_animes() -> list[Anime]:
    anime_queryset = [Anime.from_model(anime_model) for anime_model in AnimeModel.objects.all()]
    return anime_queryset
