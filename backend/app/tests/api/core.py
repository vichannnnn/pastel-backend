from app.schemas.feedback import FeedbackGetResponse, FeedbackPostResponse
from app.schemas.platform import PlatformGetResponse
from app.schemas.core import PostDataValidate
from app.schemas.sentiments import SentimentGetResponse, SentimentPostResponse
from app.schemas.tags import TagsList
from fastapi import status
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

import pytest

DATA_ENDPOINT_URL = "/data"
FILTER_ENDPOINT_URL = "/filter"
REPORT_FEEDBACK_ENDPOINT_URL = "/report_feedback"
INACCURATE_RESULT_ENDPOINT_URL = "/inaccurate_result_report"
TAG_ENDPOINT_URL = "/tag"


# Example: These parametrize will modify fixture based on params. Will go in order: ds_game first argument and
# ds_platform first argument, then ds_game second argument and ds_platform first argument then ds_game first argument
# and ds_platform second argument, ds_game second argument and ds_platform second argument Best example can be shown
# by just looking in test db's data source table

# Will use default fixture parameter in conftest.py if you don't modify it
# Example: @pytest.mark.parametrize("modified_parameter", [('test_case_1'), ('test_case_2')])
# @pytest.mark.parametrize("ds_game", [('Echolapypse'), ('fake_game')])
# @pytest.mark.parametrize("ds_platform", [('First platform'), ('second platform')])

# Below is another way of writing it without doing it by multiple mark parameters. It won't be in the above order and
# will do it one by one depending on test cases. Example: @pytest.mark.parametrize("modified_parameter,
# modified_parameter_2", [('changed_parameter_1, changed_parameter_2'), ('changed_parameter_1,
# changed_parameter_2')]) @pytest.mark.parametrize("ds_game, ds_platform", [('Echolapypse', 'First platform'),
# ('fake_game', 'second platform')])


def test_fail_data_get_endpoint(not_authenticated_client: TestClient):
    response = not_authenticated_client.get(DATA_ENDPOINT_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_fail_sentiment_get_endpoint(not_authenticated_client: TestClient):
    response = not_authenticated_client.get(INACCURATE_RESULT_ENDPOINT_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_fail_filter_endpoint(not_authenticated_client: TestClient):
    response = not_authenticated_client.get(FILTER_ENDPOINT_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_fail_report_get_endpoint(not_authenticated_client: TestClient):
    response = not_authenticated_client.get(REPORT_FEEDBACK_ENDPOINT_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_fail_tag_get_endpoint(not_authenticated_client: TestClient):
    response = not_authenticated_client.get(TAG_ENDPOINT_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_sentiment_get_endpoint(client: TestClient):
    response = client.get(INACCURATE_RESULT_ENDPOINT_URL)
    assert response.status_code == status.HTTP_200_OK
    if response.status_code == status.HTTP_200_OK:
        assert SentimentGetResponse.validate(response.json())


def test_filter_endpoint(client: TestClient):
    response = client.get(FILTER_ENDPOINT_URL)
    assert response.status_code == status.HTTP_200_OK
    if response.status_code == status.HTTP_200_OK:
        assert PlatformGetResponse.validate(response.json())


def test_report_get_endpoint(client: TestClient):
    response = client.get(REPORT_FEEDBACK_ENDPOINT_URL)
    assert response.status_code == status.HTTP_200_OK
    if response.status_code == status.HTTP_200_OK:
        assert FeedbackGetResponse.validate(response.json())


def test_tag_get_endpoint(client: TestClient):
    response = client.get(TAG_ENDPOINT_URL)
    assert response.status_code == status.HTTP_200_OK
    if response.status_code == status.HTTP_200_OK:
        assert TagsList.validate(response.json())


def test_create_tag(client: TestClient, tag):
    payload = jsonable_encoder(tag)
    response = client.post(TAG_ENDPOINT_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"tag": payload}

    response = client.post(TAG_ENDPOINT_URL, json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT
