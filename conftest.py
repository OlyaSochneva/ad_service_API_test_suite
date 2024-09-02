import pytest
import requests

from data import URL, TestData as Test
from assistant_methods import new_user_payload, create_notification_payload, return_user_ntf_id


@pytest.fixture(scope="function")
def new_user_id_and_token():
    payload = new_user_payload()
    requests.post(URL.REGISTRATION, data=payload)
    code = requests.post(URL.SEND_CODE, data={'email': payload['email']}).json()["confirmation_code"]
    token = requests.post(URL.LOGIN, data={'email': payload['email'], 'code': code}).json()["token"]
    user_id = requests.get(URL.USER_ME, headers={'Authorization': f'Bearer {token}'}).json()["id"]
    return {
        "token": token,
        "id": user_id
    }


@pytest.fixture(scope="function")
def new_notification_payload(new_user_id_and_token):
    user_id = new_user_id_and_token["id"]
    return create_notification_payload(user_id)


@pytest.fixture(scope="function")
def new_notification_id_and_user_token(new_user_id_and_token):
    user_id = new_user_id_and_token["id"]
    token = new_user_id_and_token["token"]
    payload = create_notification_payload(user_id)
    ntf_id = requests.post(URL.NOTIFICATIONS,
                           headers={'Authorization': f'Bearer {Test.ADMIN_TOKEN}'},
                           json=payload).json()["id"]
    response = requests.get(URL.NOTIFICATIONS, headers={'Authorization': f'Bearer {token}'})
    user_ntf_id = return_user_ntf_id(response.json(), ntf_id)
    return {
        "id": user_ntf_id,
        "token": new_user_id_and_token["token"]
    }


@pytest.fixture(scope="function")
def admin_token():
    code = requests.post(URL.SEND_CODE, data={'email': Test.USER_ADMIN['email']}).json()["confirmation_code"]
    token = requests.post(URL.LOGIN, data={'email': Test.USER_ADMIN['email'], 'code': code}).json()["token"]
    return token
