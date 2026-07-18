from pydantic import BaseModel

from .enums import AgeRating
from .media_schemas import MediaFullSchema, MediaSchema


class StudioSchema(BaseModel):
    mal_id: int
    name: str


class AnimeSchema(MediaSchema):
    pass


class AnimeFullSchema(MediaFullSchema, AnimeSchema):
    studios: list[StudioSchema]
    duration: str | None
    rating: AgeRating | None


class AnimeSearchSchema(BaseModel):
    data: list[AnimeSchema]
