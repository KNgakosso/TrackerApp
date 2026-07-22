from dataclasses import dataclass

from ..external.schemas.anime_schemas import AnimeFullSchema, AnimeSchema, StudioSchema
from ..models.anime_models import AnimeModel, StudioModel
from .media import Media


@dataclass
class Studio:
    mal_id: int
    name: str

    @classmethod
    def from_schema(cls, studio_schema: StudioSchema):
        return Studio(mal_id=studio_schema.mal_id, name=studio_schema.name)

    @classmethod
    def from_model(cls, studio_model: StudioModel):
        return Studio(mal_id=studio_model.mal_id, name=studio_model.name)


@dataclass
class Anime(Media):
    studios: list[Studio] | None
    duration: str | None
    rating: str | None

    def type(self):
        return "anime"

    @classmethod
    def from_schema(cls, anime_schema: AnimeSchema | AnimeFullSchema):
        studios = (
            [Studio.from_schema(studio) for studio in anime_schema.studios]
            if isinstance(anime_schema, AnimeFullSchema)
            else None
        )
        duration = (
            anime_schema.duration if isinstance(anime_schema, AnimeFullSchema) else None
        )
        rating = (
            anime_schema.rating if isinstance(anime_schema, AnimeFullSchema) else None
        )
        base = cls._base_fiedls_from_schema(anime_schema)
        return cls(**base, studios=studios, duration=duration, rating=rating)

    @classmethod
    def from_model(cls, anime_model: AnimeModel):
        base = cls._base_fields_from_model(anime_model)
        return cls(
            **base,
            studios=[Studio.from_model(studio) for studio in anime_model.studios.all()],
            duration=None,
            rating=anime_model.rating
        )
