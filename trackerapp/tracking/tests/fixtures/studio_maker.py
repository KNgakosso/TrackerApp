from typing import Callable

import pytest

from ...domain.anime import Studio
from ...external.schemas.anime_schemas import StudioSchema
from ...models.anime_models import StudioModel

StudioSchemaMaker = Callable[[], StudioSchema]
StudioMaker = Callable[[], Studio]
StudioModelMaker = Callable[[], StudioModel]


@pytest.fixture()
def studio_schema_example():
    def make_studio_schema(mal_id: int = 0, name: str = "A Studio") -> StudioSchema:
        return StudioSchema(mal_id=mal_id, name=name)

    return make_studio_schema


@pytest.fixture()
def studio_example():
    def make_studio(mal_id: int = 0, name: str = "A Studio") -> Studio:
        return Studio(mal_id=mal_id, name=name)

    return make_studio


@pytest.fixture()
def studio_model_example(db):
    def make_studio_model(mal_id: int = 0, name: str = "A Studio") -> StudioModel:
        return StudioModel.objects.create(mal_id=mal_id, name=name)

    return make_studio_model
