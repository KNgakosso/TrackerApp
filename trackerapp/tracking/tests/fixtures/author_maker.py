from typing import Callable

import pytest

from ...domain.manga import Author
from ...external.schemas.manga_schemas import AuthorSchema
from ...models.manga_models import AuthorModel

AuthorSchemaMaker = Callable[[], AuthorSchema]
AuthorMaker = Callable[[], Author]
AuthorModelMaker = Callable[[], AuthorModel]


@pytest.fixture()
def author_schema_example():
    def make_author_schema(mal_id: int = 0, name: str = "A Author") -> AuthorSchema:
        return AuthorSchema(mal_id=mal_id, name=name)

    return make_author_schema


@pytest.fixture()
def author_example():
    def make_author(mal_id: int = 0, name: str = "A Author") -> Author:
        return Author(mal_id=mal_id, name=name)

    return make_author


@pytest.fixture()
def author_model_example(db):
    def make_author_model(mal_id: int = 0, name: str = "A Author") -> AuthorModel:
        return AuthorModel.objects.create(mal_id=mal_id, name=name)

    return make_author_model
