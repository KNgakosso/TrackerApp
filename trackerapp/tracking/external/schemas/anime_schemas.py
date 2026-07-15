from .media_schemas import MediaSchema, MediaFullSchema
from pydantic import BaseModel

class StudioSchema(BaseModel):
    mal_id : int
    name : str

class AnimeSchema(MediaSchema):
    pass

class AnimeFullSchema(MediaFullSchema, AnimeSchema):
    studios : list[StudioSchema]
    duration : str
    rating : str

class AnimeSearchSchema(BaseModel):
    data : list[AnimeSchema]