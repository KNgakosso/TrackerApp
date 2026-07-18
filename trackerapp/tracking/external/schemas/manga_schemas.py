from pydantic import BaseModel

from .media_schemas import MediaFullSchema, MediaSchema


class AuthorSchema(BaseModel):
    mal_id: int
    name: str


class MangaSchema(MediaSchema):
    chapters: int | None


class MangaFullSchema(MediaFullSchema, MangaSchema):
    authors: list[AuthorSchema]


class MangaSearchSchema(BaseModel):
    data: list[MangaSchema]
