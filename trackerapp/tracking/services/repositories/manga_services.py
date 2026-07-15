from ...models import MangaModel
from ...domain.manga import Manga

def _get_manga_model(mal_id : int) -> MangaModel:
    try:
        return MangaModel.objects.get(mal_id=mal_id)
    except MangaModel.DoesNotExist:
        raise ValueError(f"Aucun manga trouvé pour l'id {mal_id}")

def get_mangas() -> list[Manga]:
    manga_queryset = [Manga.from_model(manga_model) for manga_model in MangaModel.objects.all()]
    return manga_queryset