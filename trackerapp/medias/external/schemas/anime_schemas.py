from pydantic import BaseModel, field_validator

from ...enums import AnimeRating
from .media_schemas import MediaFullSchema, MediaSchema


class StudioSchema(BaseModel):
    mal_id: int
    name: str


class AnimeSchema(MediaSchema):
    studios: list[StudioSchema]
    duration: str | None
    rating: AnimeRating | None

    @field_validator("rating", mode="before")
    @classmethod
    def handle_none_rating(cls, value):
        try:
            return AnimeRating(value)
        except ValueError:
            return None


class AnimeFullSchema(MediaFullSchema, AnimeSchema):
    pass


class AnimeSearchSchema(BaseModel):
    data: list[AnimeSchema]
