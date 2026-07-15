from pydantic import BaseModel

class EpisodeSchema(BaseModel):
    mal_id : int
    title : str
    score : float | None
    filler : bool
    recap : bool

class EpisodeFullSchema(EpisodeSchema):
    synopsis : str | None