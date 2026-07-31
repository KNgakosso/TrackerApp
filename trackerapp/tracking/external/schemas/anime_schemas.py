from pydantic import BaseModel

from ...enums import AnimeRating
from .media_schemas import MediaFullSchema, MediaSchema


class StudioSchema(BaseModel):
    mal_id: int
    name: str


class AnimeSchema(MediaSchema):
    studios: list[StudioSchema]
    duration: str | None
    rating: AnimeRating | None


class AnimeFullSchema(MediaFullSchema, AnimeSchema):
    pass


class AnimeSearchSchema(BaseModel):
    data: list[AnimeSchema]
