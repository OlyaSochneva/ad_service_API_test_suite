import pytest
import requests

from data import URL, TestData as Test
from assistant_methods import return_user_ntf_id
from payloads import new_user_payload, notification_payload, new_card_payload, new_service_card_payload


@pytest.fixture(scope="session")
def admin_token():
    code = requests.post(URL.SEND_CODE, data={'email': Test.USER_ADMIN['email']}).json()["confirmation_code"]
    access_token = requests.post(URL.LOGIN, data={'email': Test.USER_ADMIN['email'], 'code': code}).json()["access"]
    return access_token


@pytest.fixture(scope="session")
def user_token():
    payload = new_user_payload()
    requests.post(URL.REGISTRATION, data=payload)
    code = requests.post(URL.SEND_CODE, data={'email': payload['email']}).json()["confirmation_code"]
    access_token = requests.post(URL.LOGIN, data={'email': payload['email'], 'code': code}).json()["access"]
    return access_token


@pytest.fixture(scope="session")
def user_id(user_token):
    user_id = requests.get(URL.USER_ME, headers={'Authorization': f'Bearer {user_token}'}).json()["id"]
    return user_id


@pytest.fixture(scope="session")
def basic_card(user_token):
    payload = new_card_payload()
    card_id = requests.post(URL.CARDS, headers={'Authorization': f'Bearer {user_token}'},
                            json=payload).json()["id"]
    return {
        "id": card_id,
        "token": user_token
    }


@pytest.fixture(scope="session")
def notification(admin_token, user_token):
    user_id = requests.get(URL.USER_ME, headers={'Authorization': f'Bearer {user_token}'}).json()["id"]
    payload = notification_payload(user_id)
    ntf_id = requests.post(URL.NOTIFICATIONS,
                           headers={'Authorization': f'Bearer {admin_token}'},
                           json=payload).json()["id"]
    response = requests.get(URL.NOTIFICATIONS, headers={'Authorization': f'Bearer {user_token}'})
    user_ntf_id = return_user_ntf_id(response.json(), ntf_id)
    return {
        "id": user_ntf_id,
        "token": user_token
    }


# @pytest.fixture(scope="function")
# def new_user_id_and_token():
# payload = new_user_payload()
# requests.post(URL.REGISTRATION, data=payload)
# code = requests.post(URL.SEND_CODE, data={'email': payload['email']}).json()["confirmation_code"]
# refresh_token = requests.post(URL.LOGIN, data={'email': payload['email'], 'code': code}).json()["refresh"]
# user_id = requests.get(URL.USER_ME, headers={'Authorization': f'Bearer {refresh_token}'}).json()["id"]
# return {
# "token": refresh_token,
# "id": user_id
# }


#@pytest.fixture(scope="function")
#def new_card_id_and_token(new_user_id_and_token):
    #token = new_user_id_and_token["token"]
    #payload = new_card_payload()
    #card_id = requests.post(URL.CARDS, headers={'Authorization': f'Bearer {token}'}, json=payload).json()["id"]
    #return {
        #"card_id": card_id,
        #"token": token
    #}


@pytest.fixture(scope="function")
def new_service_card_id_and_token(new_user_id_and_token):
    token = new_user_id_and_token["token"]
    payload = new_service_card_payload()
    card_id = requests.post(URL.SERVICE_CARDS, headers={'Authorization': f'Bearer {token}'}, json=payload).json()["id"]
    return {
        "card_id": card_id,
        "token": token
    }

# @pytest.fixture(scope="function")
# def new_notification_payload(new_user_id_and_token):
# user_id = new_user_id_and_token["id"]
# return notification_payload(user_id)


# @pytest.fixture(scope="function")
# def new_notification_id_and_user_token(new_user_id_and_token):
# user_id = new_user_id_and_token["id"]
# token = new_user_id_and_token["token"]
# payload = notification_payload(user_id)
# ntf_id = requests.post(URL.NOTIFICATIONS,
# headers={'Authorization': f'Bearer {Test.ADMIN_TOKEN}'},
# json=payload).json()["id"]
# response = requests.get(URL.NOTIFICATIONS, headers={'Authorization': f'Bearer {token}'})
# user_ntf_id = return_user_ntf_id(response.json(), ntf_id)
# return {
# "id": user_ntf_id,
# "token": new_user_id_and_token["token"]
# }
