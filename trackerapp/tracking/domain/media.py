from dataclasses import dataclass

from ..enums import MediaCompletion, MediaStatus
from ..external.schemas.media_schemas import (
    DemographicSchema,
    GenreSchema,
    ImagesUrlsSchema,
    MediaFullSchema,
    MediaSchema,
    ThemeSchema,
)
from ..models.media_models import DemographicModel, GenreModel, MediaModel, ThemeModel
from ..utils import MODEL_TO_DOMAIN


@dataclass
class ImagesUrls:
    small_image_url: str | None
    image_url: str | None
    large_image_url: str | None

    @classmethod
    def from_schema(cls, images_urls_schema: ImagesUrlsSchema):
        return ImagesUrls(
            small_image_url=images_urls_schema.small_image_url,
            image_url=images_urls_schema.image_url,
            large_image_url=images_urls_schema.large_image_url,
        )


@dataclass
class Genre:
    name: str

    @classmethod
    def from_schema(cls, genre_schema: GenreSchema):
        return Genre(name=genre_schema.name)

    @classmethod
    def from_model(cls, genre_model: GenreModel):
        return Genre(name=genre_model.name)


@dataclass
class Theme:
    name: str

    @classmethod
    def from_schema(cls, theme_schema: ThemeSchema):
        return Theme(name=theme_schema.name)

    @classmethod
    def from_model(cls, theme_model: ThemeModel):
        return Theme(name=theme_model.name)


@dataclass
class Demographic:
    name: str

    @classmethod
    def from_schema(cls, demographic_schema: DemographicSchema):
        return Demographic(name=demographic_schema.name)

    @classmethod
    def from_model(cls, demographic_model: DemographicModel):
        return Demographic(name=demographic_model.name)


"""
@dataclass
class Relations():
    type : str

    @classmethod
    def from_schema(cls, relation_schema : list[RelationSchema]):
        return Relations(
            type = relation_schema.relation
            #A COMPLETER
        )
    @classmethod
    def from_model(cls, relation_model : RelationModel):
        return Relations(
            type = relation_model.relation_type
            #A COMPLETER
        )
"""


@dataclass
class Media:
    mal_id: int
    title: str
    images_urls: ImagesUrls | None
    format: str | None
    synopsis: str | None
    score: float | None
    rank: int | None
    themes: list[Theme]
    genres: list[Genre]
    demographics: list[Demographic]
    number_sections: int | None
    # relations : list[Relations] | None
    status: MediaStatus | None
    user_score: int | None
    user_completion: MediaCompletion
    user_current_section: int | None

    def type(self):
        raise NotImplementedError

    @classmethod
    def from_model(cls, media_model: MediaModel):
        media_cls = MODEL_TO_DOMAIN[type(media_model)]
        return media_cls.from_model(media_model)

    @classmethod
    def _base_fields_from_schema(cls, media_schema: MediaSchema | MediaFullSchema):
        # relations = Relations.from_schema(media_schema.relations) if isinstance(media_schema, MediaFullSchema) else None
        return {
            "mal_id": media_schema.mal_id,
            "title": media_schema.title,
            "images_urls": ImagesUrls.from_schema(media_schema.images.webp),
            "format": media_schema.format,
            "synopsis": media_schema.synopsis,
            "score": media_schema.score,
            "rank": media_schema.rank,
            "themes": [Theme.from_schema(theme) for theme in media_schema.themes],
            "genres": [Genre.from_schema(genre) for genre in media_schema.genres],
            "demographics": [
                Demographic.from_schema(demographic)
                for demographic in media_schema.demographics
            ],
            "number_sections": media_schema.number_sections,
            # "relations": relations,
            "status": media_schema.status,
            "user_score": None,
            "user_completion": MediaCompletion.NOT_STARTED,
            "user_current_section": None if media_schema.number_sections is None else 0,
        }

    @classmethod
    def _base_fields_from_model(cls, media_model: MediaModel):
        def none_if_empty(string: str) -> str | None:
            return None if string == "" else string

        return {
            "mal_id": media_model.mal_id,
            "title": media_model.title,
            "images_urls": ImagesUrls(
                small_image_url=none_if_empty(media_model.small_image_url),
                image_url=none_if_empty(media_model.image_url),
                large_image_url=none_if_empty(media_model.large_image_url),
            ),
            "format": none_if_empty(media_model.format),
            "synopsis": none_if_empty(media_model.synopsis),
            "score": media_model.score,
            "rank": media_model.rank,
            "themes": [Theme.from_model(theme) for theme in media_model.themes.all()],
            "genres": [Genre.from_model(genre) for genre in media_model.genres.all()],
            "demographics": [
                Demographic.from_model(demographic)
                for demographic in media_model.demographics.all()
            ],
            "number_sections": media_model.number_sections,
            # "relations": [Relations.from_model(relation) for relation in media_model.relations.all()],
            "status": (
                None if media_model.status == "" else MediaStatus(media_model.status)
            ),
            "user_score": media_model.user_score,
            "user_completion": MediaCompletion(media_model.user_completion),
            "user_current_section": media_model.user_current_section,
        }

    def complete_next(self) -> int | None:
        if self.number_sections is None:
            return None
        if (
            not self.user_current_section is None
            and self.user_current_section < self.number_sections
        ):
            self.user_current_section += 1
        self._update_media_completion()

    def complete(self):
        self.user_completion = MediaCompletion.COMPLETED
        if not self.number_sections is None:
            self.user_current_section = self.number_sections

    def restart(self):
        self.user_completion = MediaCompletion.NOT_STARTED
        if not self.number_sections is None:
            self.user_current_section = 0

    def define_current_section(self, new_current_section: int):
        if not self.number_sections is None:
            if new_current_section >= 0 and new_current_section < self.number_sections:
                self.user_current_section = new_current_section
        self._update_media_completion()

    def _update_media_completion(self):
        if not self.number_sections is None and not self.user_current_section is None:
            if self.user_current_section == 0:
                self.user_completion = MediaCompletion.NOT_STARTED
            elif self.user_current_section == self.number_sections:
                self.user_completion = MediaCompletion.COMPLETED
            elif (
                self.user_current_section > 0
                and self.user_current_section < self.number_sections
            ):
                self.user_completion = MediaCompletion.IN_PROGRESS
            else:
                raise ValueError()
