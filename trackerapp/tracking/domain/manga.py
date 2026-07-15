from dataclasses import dataclass

from ..external.schemas.manga_schemas import AuthorSchema, MangaFullSchema, MangaSchema
from ..models.manga_models import AuthorModel, MangaModel
from .media import Media


@dataclass
class Author:
    name: str
    mal_id: int

    @classmethod
    def from_schema(cls, author: AuthorSchema):
        return Author(name=author.name, mal_id=author.mal_id)

    @classmethod
    def from_model(cls, author: AuthorModel):
        return Author(name=author.name, mal_id=author.mal_id)


@dataclass
class Manga(Media):
    number_chapters: int | None

    authors: list[Author] | None

    def type(self):
        return "manga"

    @classmethod
    def from_schema(cls, manga_schema: MangaSchema | MangaFullSchema):
        authors = (
            [Author.from_schema(author) for author in manga_schema.authors]
            if isinstance(manga_schema, MangaFullSchema)
            else None
        )
        base = cls._base_fiedls_from_schema(manga_schema)
        return cls(**base, number_chapters=manga_schema.chapters, authors=authors)

    @classmethod
    def from_model(cls, manga_model: MangaModel):
        base = cls._base_fields_from_model(manga_model)
        return cls(
            **base,
            authors=[Author.from_model(author) for author in manga_model.authors.all()],
            number_chapters=manga_model.number_volumes
        )
