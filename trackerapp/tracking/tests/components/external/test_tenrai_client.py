import pytest
import requests
from tracking.external.api_client import tenrai_client as tenrai
from tracking.external.exceptions import ExternalApiError

# TESTS _GET
############################################


@pytest.mark.parametrize(
    "params", [{}, {"min_score": 5}, {"q": "Titre", "field": "value"}, None]
)
def test_get_OK(mocker, params):
    response = mocker.Mock()
    response.json.return_value = {"data": {"title": "Titre", "mal_id": 0}}
    mock_requests_get = mocker.patch(
        "tracking.external.api_client.tenrai_client.requests.get", return_value=response
    )
    data = tenrai._get("/path", params=params)
    assert data == {"title": "Titre", "mal_id": 0}
    mock_requests_get.assert_called_once_with(
        f"{tenrai.BASE_URL}/path", params=params, timeout=10
    )


def test_get_request_exception(mocker):
    response = mocker.Mock()
    response.json.return_value = {"data": {"title": "Titre", "mal_id": 0}}
    response.raise_for_status.side_effect = requests.RequestException()
    mocker.patch(
        "tracking.external.api_client.tenrai_client.requests.get", return_value=response
    )
    with pytest.raises(ExternalApiError) as e:
        tenrai._get("/path", params={"min_score": 5})
    assert str(e.value) == "Tenrai API is unavailable."


def test_get_value_error(mocker):
    response = mocker.Mock()
    response.json.return_value = {"data": {"title": "Titre", "mal_id": 0}}
    response.json.side_effect = ValueError()
    mocker.patch(
        "tracking.external.api_client.tenrai_client.requests.get", return_value=response
    )
    params = {"min_score": 5}
    with pytest.raises(ExternalApiError) as e:
        tenrai._get("/path", params=params)
    assert (
        str(e.value)
        == f"Invalid API response format for path : /path, params : {params}."
    )


def test_get_key_error(mocker):
    class FakeJson:
        def __getitem__(self, key):
            raise KeyError(key)

    response = mocker.Mock()
    response.json.return_value = FakeJson()
    mocker.patch(
        "tracking.external.api_client.tenrai_client.requests.get", return_value=response
    )
    params = {"min_score": 5}
    with pytest.raises(ExternalApiError) as e:
        tenrai._get("/path", params=params)
    assert (
        str(e.value)
        == f"Invalid API response format for path : /path, params : {params}."
    )


# TESTS GET_ANIME_RESEARCH_LIST
############################################
@pytest.mark.parametrize("params", [{"q": "Naruto"}, {}, None])
def test_get_anime_research_list(mocker, params):
    data = [{"animeschema 1": 1}, {"anime_schema_2": 2}]
    _get_mock = mocker.patch(
        "tracking.external.api_client.tenrai_client._get", return_value=data
    )
    mocker.patch(
        "tracking.external.api_client.tenrai_client.AnimeSearchSchema",
        side_effect=lambda data: f"AnimeSearchSchema({data})",
    )
    anime_research_schema = tenrai.get_anime_research_list(params=params)

    _get_mock.assert_called_once_with(path="/anime", params=params)
    assert anime_research_schema == f"AnimeSearchSchema({data})"


# TESTS GET_MANGA_RESEARCH_LIST
############################################
@pytest.mark.parametrize("params", [{"q": "Naruto"}, {}, None])
def test_get_manga_research_list(mocker, params):
    data = [{"mangaschema 1": 1}, {"manga_schema_2": 2}]
    _get_mock = mocker.patch(
        "tracking.external.api_client.tenrai_client._get", return_value=data
    )
    mocker.patch(
        "tracking.external.api_client.tenrai_client.MangaSearchSchema",
        side_effect=lambda data: f"MangaSearchSchema({data})",
    )
    manga_research_schema = tenrai.get_manga_research_list(params=params)

    _get_mock.assert_called_once_with(path="/manga", params=params)
    assert manga_research_schema == f"MangaSearchSchema({data})"


# TESTS GET_ANIME
############################################
def test_get_anime(mocker):
    data = {"mal_id": 0, "title": "anime"}
    _get_mock = mocker.patch(
        "tracking.external.api_client.tenrai_client._get", return_value=data
    )
    mocker.patch(
        "tracking.external.api_client.tenrai_client.AnimeSchema",
        side_effect=lambda **data: f"AnimeSchema(**{data})",
    )
    anime_schema = tenrai.get_anime(0)

    _get_mock.assert_called_once_with(path="/anime/0")
    assert anime_schema == f"AnimeSchema(**{data})"


# TESTS GET_ANIME_FULL
############################################


def test_get_anime_full(mocker):
    data = {"mal_id": 12345, "title": "anime"}
    _get_mock = mocker.patch(
        "tracking.external.api_client.tenrai_client._get", return_value=data
    )
    mocker.patch(
        "tracking.external.api_client.tenrai_client.AnimeFullSchema",
        side_effect=lambda **data: f"AnimeFullSchema(**{data})",
    )
    anime_full_schema = tenrai.get_anime_full(12345)

    _get_mock.assert_called_once_with(path="/anime/12345/full")
    assert anime_full_schema == f"AnimeFullSchema(**{data})"


# TESTS GET_MANGA
############################################
def test_get_manga(mocker):
    data = {"mal_id": 2, "title": "manga"}
    _get_mock = mocker.patch(
        "tracking.external.api_client.tenrai_client._get", return_value=data
    )
    mocker.patch(
        "tracking.external.api_client.tenrai_client.MangaSchema",
        side_effect=lambda **data: f"MangaSchema(**{data})",
    )
    manga_schema = tenrai.get_manga(2)

    _get_mock.assert_called_once_with(path="/manga/2")
    assert manga_schema == f"MangaSchema(**{data})"


# TESTS GET_MANGA_FULL
############################################


def test_get_manga_full(mocker):
    data = {"mal_id": 949, "title": "manga"}
    _get_mock = mocker.patch(
        "tracking.external.api_client.tenrai_client._get", return_value=data
    )
    mocker.patch(
        "tracking.external.api_client.tenrai_client.MangaFullSchema",
        side_effect=lambda **data: f"MangaFullSchema(**{data})",
    )
    manga_full_schema = tenrai.get_manga_full(949)

    _get_mock.assert_called_once_with(path="/manga/949/full")
    assert manga_full_schema == f"MangaFullSchema(**{data})"


# TESTS GET_EPISODE
############################################


def test_get_episode(mocker):
    data = {"episode_id": 10, "title": "Titre de l'épisode"}
    _get_mock = mocker.patch(
        "tracking.external.api_client.tenrai_client._get", return_value=data
    )
    mocker.patch(
        "tracking.external.api_client.tenrai_client.EpisodeSchema",
        side_effect=lambda **data: f"EpisodeSchema(**{data})",
    )
    episode_schema = tenrai.get_episode(anime_mal_id=488, episode_mal_id=10)

    _get_mock.assert_called_once_with(path="/anime/488/episodes/10")
    assert episode_schema == f"EpisodeSchema(**{data})"


# TESTS GET_EPISODE_LIST
############################################


def test_get_episode_list(mocker):
    data = [
        {"episode_id": 1, "title": "Titre de l'épisode 1"},
        {"episode_id": 2, "title": "Titre de l'épisode 2"},
        {"episode_id": 3, "title": "Titre de l'épisode 3"},
    ]
    _get_mock = mocker.patch(
        "tracking.external.api_client.tenrai_client._get", return_value=data
    )
    mocker.patch(
        "tracking.external.api_client.tenrai_client.EpisodeSchema",
        side_effect=lambda **data: f"EpisodeSchema(**{data})",
    )
    episode_list_schema = tenrai.get_episodes_list(anime_mal_id=488)

    _get_mock.assert_called_once_with(path="/anime/488/episodes")
    assert episode_list_schema == [
        f"EpisodeSchema(**{data[0]})",
        f"EpisodeSchema(**{data[1]})",
        f"EpisodeSchema(**{data[2]})",
    ]
