from fastapi import status
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.schemas import authentication

CREATE_ACCOUNT_ENDPOINT_URL = "/create"
LOGIN_ENDPOINT_URL = "/auth/login"
GET_INFO_ENDPOINT_URL = "/get_info"


def test_create_endpoint(
    test_authentication_client: TestClient,
    correct_login_user: authentication.UserSchema,
):
    payload = jsonable_encoder(correct_login_user)
    response = test_authentication_client.post(
        CREATE_ACCOUNT_ENDPOINT_URL, json=payload
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "username": correct_login_user.username,
        "status": "Successfully created account.",
    }


def test_login_endpoint(
    test_authentication_client: TestClient,
    correct_login_user: authentication.UserSchema,
    wrong_login_user: authentication.UserSchema,
):
    payload = jsonable_encoder(correct_login_user)
    response = test_authentication_client.post(LOGIN_ENDPOINT_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK

    payload = jsonable_encoder(wrong_login_user)
    response = test_authentication_client.post(LOGIN_ENDPOINT_URL, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_account_name_endpoint(
    test_authentication_client: TestClient,
    correct_login_user: authentication.UserSchema,
):
    payload = jsonable_encoder(correct_login_user)
    response = test_authentication_client.post(LOGIN_ENDPOINT_URL, json=payload)
    access_token = response.json()["access_token"]
    test_authentication_client.headers.update(
        {"Authorization": f"Bearer {access_token}"}
    )
    response = test_authentication_client.get(url=GET_INFO_ENDPOINT_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"username": correct_login_user.username}
