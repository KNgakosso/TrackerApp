from dataclasses import dataclass

from ..external.schemas.media_schemas import (
    DemographicSchema,
    GenreSchema,
    ImagesSchema,
    ImagesUrlsSchema,
    MediaFullSchema,
    MediaSchema,
    ThemeSchema,
)
from ..models.media_models import (
    DemographicModel,
    GenreModel,
    ImagesModel,
    MediaModel,
    ThemeModel,
)


@dataclass
class ImagesUrls:
    small_image_url: str
    medium_image_url: str
    large_image_url: str

    @classmethod
    def from_schema(cls, images_urls_schema: ImagesUrlsSchema):
        return ImagesUrls(
            small_image_url=images_urls_schema.small_image_url,
            medium_image_url=images_urls_schema.image_url,
            large_image_url=images_urls_schema.large_image_url,
        )

    @classmethod
    def from_model(cls, images_urls_model: ImagesModel):
        return ImagesUrls(
            small_image_url=images_urls_model.small_image_url,
            medium_image_url=images_urls_model.medium_image_url,
            large_image_url=images_urls_model.large_image_url,
        )


@dataclass
class Images:
    webp: ImagesUrls | None
    jpg: ImagesUrls | None

    @classmethod
    def from_schema(cls, images_schema: ImagesSchema):
        return Images(
            webp=ImagesUrls.from_schema(images_schema.webp),
            jpg=ImagesUrls.from_schema(images_schema.jpg),
        )

    @classmethod
    def from_model(cls, images_model: ImagesModel):
        return Images(webp=ImagesUrls.from_model(images_model), jpg=None)


@dataclass
class Genre:
    # mal_id : int
    name: str

    @classmethod
    def from_schema(cls, genre_schema: GenreSchema):
        return Genre(
            # mal_id = genre_schema.mal_id,
            name=genre_schema.name
        )

    @classmethod
    def from_model(cls, genre_model: GenreModel):
        return Genre(
            # mal_id = genre_model.mal_id,
            name=genre_model.name
        )


@dataclass
class Theme:
    # mal_id : int
    name: str

    @classmethod
    def from_schema(cls, theme_schema: ThemeSchema):
        return Theme(
            # mal_id = theme_schema.mal_id,
            name=theme_schema.name
        )

    @classmethod
    def from_model(cls, theme_model: ThemeModel):
        return Theme(
            # mal_id = theme_model.mal_id,
            name=theme_model.name
        )


@dataclass
class Demographic:
    name: str

    # mal_id : int
    @classmethod
    def from_schema(cls, demographic_schema: DemographicSchema):
        return Demographic(
            # mal_id = demographic_schema.mal_id,
            name=demographic_schema.name
        )

    @classmethod
    def from_model(cls, demographic_model: DemographicModel):
        return Demographic(
            # mal_id = demographic_model.mal_id,
            name=demographic_model.name
        )


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
    images: Images
    title: str
    score: float | None
    synopsis: str | None
    number_sections: int | None
    rank: int | None
    themes: list[Theme]
    genres: list[Genre]
    demographics: list[Demographic]
    # relations : list[Relations] | None
    status: str | None
    user_score: float | None
    user_completion: str
    user_current_section: int

    def type(self):
        raise NotImplementedError

    @classmethod
    def _base_fiedls_from_schema(cls, media_schema: MediaSchema | MediaFullSchema):
        # relations = Relations.from_schema(media_schema.relations) if isinstance(media_schema, MediaFullSchema) else None
        status = (
            media_schema.status if isinstance(media_schema, MediaFullSchema) else None
        )
        return {
            "mal_id": media_schema.mal_id,
            "images": Images.from_schema(media_schema.images),
            "title": media_schema.title,
            "score": media_schema.score,
            "synopsis": media_schema.synopsis,
            "number_sections": media_schema.number_sections,
            "rank": media_schema.rank,
            "themes": [Theme.from_schema(theme) for theme in media_schema.themes],
            "genres": [Genre.from_schema(genre) for genre in media_schema.genres],
            "demographics": [
                Demographic.from_schema(demographic)
                for demographic in media_schema.demographics
            ],
            # "relations": relations,
            "status": status,
            "user_score": None,
            "user_completion": "Unseen",
            "user_current_section": 0,
        }

    @classmethod
    def _base_fields_from_model(cls, media_model: MediaModel):
        return {
            "mal_id": media_model.mal_id,
            "images": Images.from_model(media_model.images),
            "title": media_model.title,
            "score": media_model.score,
            "synopsis": media_model.synopsis,
            "number_sections": media_model.number_sections,
            "rank": media_model.rank,
            "themes": [Theme.from_model(theme) for theme in media_model.themes.all()],
            "genres": [Genre.from_model(genre) for genre in media_model.genres.all()],
            "demographics": [
                Demographic.from_model(demographic)
                for demographic in media_model.demographics.all()
            ],
            # "relations": [Relations.from_model(relation) for relation in media_model.relations.all()],
            "status": media_model.status,
            "user_score": media_model.user_score,
            "user_completion": media_model.user_completion,
            "user_current_section": media_model.user_current_section,
        }
