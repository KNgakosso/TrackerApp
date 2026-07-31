from dataclasses import dataclass

from ..models.watchlist_model import WatchlistModel
from ..utils import MODEL_TO_DOMAIN
from .media import Media


@dataclass
class Watchlist:
    name: str
    medias: list[Media]

    @classmethod
    def from_model(cls, watchlist_model: WatchlistModel):
        return Watchlist(
            name=watchlist_model.name,
            medias=[
                MODEL_TO_DOMAIN[type(media_model)].from_model(media_model)
                for media_model in watchlist_model.medias.all()
            ],
        )
