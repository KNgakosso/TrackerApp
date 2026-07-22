from dataclasses import dataclass

from ..external.schemas.episodes_schemas import EpisodeFullSchema, EpisodeSchema
from ..models.anime_models import EpisodeModel


@dataclass
class Episode:
    mal_id: int
    title: str
    score: float | None
    filler: bool
    recap: bool
    synopsis: str | None
    user_score: float | None
    user_completion: str

    @classmethod
    def from_schema(cls, episode_schema: EpisodeSchema | EpisodeFullSchema):
        synopsis = (
            episode_schema.synopsis
            if isinstance(episode_schema, EpisodeFullSchema)
            else None
        )
        return Episode(
            mal_id=episode_schema.mal_id,
            title=episode_schema.title,
            score=episode_schema.score,
            filler=episode_schema.filler,
            recap=episode_schema.recap,
            synopsis=synopsis,
            user_score=None,
            user_completion="Unseen",
        )

    @classmethod
    def from_model(cls, episode_model: EpisodeModel):
        return Episode(
            mal_id=episode_model.mal_id,
            title=episode_model.title,
            score=episode_model.score,
            filler=episode_model.filler,
            recap=episode_model.recap,
            synopsis=episode_model.synopsis,
            user_score=episode_model.user_score,
            user_completion=episode_model.user_completion,
        )
