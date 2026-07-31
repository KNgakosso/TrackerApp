from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from ...enums import MediaStatus


class ImagesUrlsSchema(BaseModel):
    small_image_url: str | None
    image_url: str | None
    large_image_url: str | None


class ImagesSchema(BaseModel):
    webp: ImagesUrlsSchema
    jpg: ImagesUrlsSchema


class GenreSchema(BaseModel):
    mal_id: int
    name: str


class ThemeSchema(BaseModel):
    mal_id: int
    name: str


class DemographicSchema(BaseModel):
    mal_id: int
    name: str


"""
class RelationSchema(BaseModel):
    relation : str
    entry : list[MediaShortSchema]
"""


class MediaSchema(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)
    # model_config pour utiliser les attributs sans utiliser leurs alias
    mal_id: int
    title: str = Field(validation_alias=AliasChoices("title", "name"))
    images: ImagesSchema
    format: str | None = Field(alias="type")
    synopsis: str | None
    score: float | None
    rank: int | None
    themes: list[ThemeSchema]
    genres: list[GenreSchema]
    demographics: list[DemographicSchema]
    number_sections: int | None = Field(
        validation_alias=AliasChoices("episodes", "volumes")
    )
    status: MediaStatus | None  # State of the Publication / Diffusion


class MediaFullSchema(MediaSchema):
    pass
    # relations : list[RelationSchema]
