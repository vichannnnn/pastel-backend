from datetime import datetime

from app.schemas.follower_count import FollowerCountGetResponse

# from app.schemas.official_posts import OfficialPostsGraphSchema
from app.schemas.sentiments import SentimentDataSchema, SentimentTrendDataSchema

# from app.schemas.stats import OfficialPostStatisticsSchema
from fastapi import status
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
import pytest

SENTIMENT_STATS_URL = "/stats/aggregate_sentiment"
POSTS_ENDPOINT_URL = "/stats/official_post_statistics"
OFFICIAL_ENDPOINT_URL = "/stats/official_post_graph"
FOLLOWER_STATS_URL = "/stats/official_page_followers_count"
SENTIMENT_STATS_TREND_URL = "/stats/sentiment_trend"


def test_fail_get_sentiment_stats(not_authenticated_client: TestClient):
    response = not_authenticated_client.get(SENTIMENT_STATS_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_official_post_statistics_endpoint(not_authenticated_client: TestClient):
    response = not_authenticated_client.get(POSTS_ENDPOINT_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_fail_official_get_endpoint(not_authenticated_client: TestClient):
    response = not_authenticated_client.get(OFFICIAL_ENDPOINT_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_fail_followers_stats_endpoint(not_authenticated_client: TestClient):
    response = not_authenticated_client.get(FOLLOWER_STATS_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_fail_get_sentiment_trend(not_authenticated_client: TestClient):
    response = not_authenticated_client.get(SENTIMENT_STATS_TREND_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# def test_sentiment_stats_endpoint(client: TestClient):
#     import random
#     from datetime import datetime, timedelta
#
#     test = [
#         {
#             1: {"Game": "Echocalypse", "Region": "Japan"},
#             2: {
#                 "Game": "Echocalypse",
#                 "Region": "South East Asia",
#             },
#             3: {
#                 "Game": "Echocalypse",
#                 "Region": "Global",
#             },
#             4: {"Game": "Echocalypse", "Region": "China"},
#             5: {"Game": "Time Raiders", "Region": "Japan"},
#             6: {
#                 "Game": "Time Raiders",
#                 "Region": "South East Asia",
#             },
#             7: {
#                 "Game": "Time Raiders",
#                 "Region": "Global",
#             },
#             8: {"Game": "Time Raiders", "Region": "China"},
#         }
#     ]
#
#     all_data = test[0]
#     for i in range(1, len(all_data) + 1):
#         ran_platform = random.choice(
#             ["Facebook", "Baidu Tieba", "Twitter", "Discord", "TapTap"]
#         )
#         curr_test = all_data[i]
#
#         end_date = datetime.now()
#         curr_day = int(end_date.strftime("%d"))
#         ran_day = random.randint(1, curr_day - 1)
#         start_date = end_date - timedelta(days=ran_day)
#
#         region = curr_test["Region"]
#         game = curr_test["Game"]
#         link = f"{SENTIMENT_STATS_URL}?platforms={ran_platform}&countries={region}&game={game}&time={start_date.strftime('%Y-%m-%d')}&time={end_date.strftime('%Y-%m-%d')}".replace(
#             " ", "%20"
#         )
#
#         response = client.get(link)
#         sentiment_res = response.json()["data"][0]
#
#         total_sentiment = (
#             sentiment_res["positive"]
#             + sentiment_res["negative"]
#             + sentiment_res["neutral"]
#         )
#
#         # 0.0 Happens if no data is found
#         if total_sentiment != 0.0:
#             assert 0.9999 <= round(total_sentiment, 4) <= 1.0001


# def test_posts_get_endpoint(client: TestClient):
#     test_cases = [
#         {
#             "data": {},
#             "expected_status_code": status.HTTP_200_OK,
#         },
#         {
#             "data": {
#                 "platforms": ["Twitter"],
#             },
#             "expected_status_code": status.HTTP_200_OK,
#         },
#         {
#             "data": {
#                 "countries": ["Global"],
#             },
#             "expected_status_code": status.HTTP_200_OK,
#         },
#         {
#             "data": {
#                 "games": ["Echocalypse"],
#             },
#             "expected_status_code": status.HTTP_200_OK,
#         },
#         {
#             "data": {
#                 "time": ["2023-01-06", "2023-01-09"],
#             },
#             "expected_status_code": status.HTTP_200_OK,
#         },
#         {
#             "data": {
#                 "time": ["string", "Wrong Date Format"],
#             },
#             "expected_status_code": 400,
#         },
#     ]
#
#     for test_case in test_cases:
#         response = client.get(POSTS_ENDPOINT_URL, params=test_case["data"])  # type: ignore
#         assert response.status_code == test_case["expected_status_code"]
#         if response.status_code == status.HTTP_200_OK:
#             assert OfficialPostsGraphSchema.validate(response.json())
#
#
# def test_official_get_endpoint(client: TestClient):
#     test_cases = [
#         {
#             "data": {},
#             "expected_status_code": status.HTTP_200_OK,
#         },
#         {
#             "data": {
#                 "platforms": ["Twitter"],
#             },
#             "expected_status_code": status.HTTP_200_OK,
#         },
#         {
#             "data": {
#                 "countries": ["Global"],
#             },
#             "expected_status_code": status.HTTP_200_OK,
#         },
#         {
#             "data": {
#                 "games": ["Echocalypse"],
#             },
#             "expected_status_code": status.HTTP_200_OK,
#         },
#         {
#             "data": {
#                 "time": ["2023-01-06", "2023-01-09"],
#             },
#             "expected_status_code": status.HTTP_200_OK,
#         },
#         {
#             "data": {
#                 "time": ["string", "Wrong Date Format"],
#             },
#             "expected_status_code": 400,
#         },
#     ]
#
#     for test_case in test_cases:
#         response = client.get(OFFICIAL_ENDPOINT_URL, params=test_case["data"])  # type: ignore
#         assert response.status_code == test_case["expected_status_code"]
#         if response.status_code == status.HTTP_200_OK:
#             assert OfficialPostStatisticsSchema.validate(response.json())


def test_get_sentiment_stats_endpoint(client: TestClient):
    response = client.get(SENTIMENT_STATS_URL)
    res = response.json()
    assert response.status_code == status.HTTP_200_OK

    if response.status_code == status.HTTP_200_OK:
        assert SentimentDataSchema.validate(res)


# Newly rewritten test_get_followers_stats_endpoint
@pytest.mark.parametrize("follower_stat_time", [("2001-12-1", "2001-12-5"), ("", "")])
def test_get_followers_stats_endpoint(
    client: TestClient, follower_stat, follower_stat_time
):
    payload = jsonable_encoder(follower_stat)
    response = client.get(FOLLOWER_STATS_URL, params=payload)
    res = response.json()

    start_date, end_date = follower_stat_time
    if isinstance(start_date, str) and isinstance(end_date, str):
        try:
            datetime.strptime(start_date, "%Y-%m-%d").date()
            datetime.strptime(end_date, "%Y-%m-%d").date()

        except ValueError:
            assert response.status_code == status.HTTP_400_BAD_REQUEST

        else:
            assert response.status_code == status.HTTP_200_OK
            if response.status_code == status.HTTP_200_OK:
                assert FollowerCountGetResponse.validate(res)

    print("sanity check:", res)


# def test_get_followers_stats_endpoint(client: TestClient):
#    test_cases = [
#        {
#            "data": {"platforms": [], "countries": [], "games": [], "time": []},
#            "expected_status_code": status.HTTP_200_OK,
#        },
#        {
#            "data": {
#                "platforms": [],
#                "countries": [],
#                "games": [],
#                "time": ["string", "Wrong Date Format"],
#            },
#            "expected_status_code": status.HTTP_400_BAD_REQUEST,
#        },
#    ]
#
#    for test_case in test_cases:
#        response = client.get(FOLLOWER_STATS_URL, params=test_case["data"])  # type: ignore
#        assert response.status_code == test_case["expected_status_code"]
#        if response.status_code == status.HTTP_200_OK:
#            assert FollowerCountGetResponse.validate(response.json())


def test_get_sentiment_trend_endpoint(client: TestClient):
    response = client.get(SENTIMENT_STATS_TREND_URL)
    res = response.json()
    assert response.status_code == status.HTTP_200_OK

    if response.status_code == status.HTTP_200_OK:
        assert SentimentTrendDataSchema.validate(res)
