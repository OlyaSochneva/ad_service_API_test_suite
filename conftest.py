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


@pytest.fixture(scope="function")
def user_refresh_token():
    payload = new_user_payload()
    requests.post(URL.REGISTRATION, data=payload)
    code = requests.post(URL.SEND_CODE, data={'email': payload['email']}).json()["confirmation_code"]
    refresh_token = requests.post(URL.LOGIN, data={'email': payload['email'], 'code': code}).json()["refresh"]
    return refresh_token


@pytest.fixture(scope="session")
def user_id(user_token):
    user_id = requests.get(URL.USER_ME, headers={'Authorization': f'Bearer {user_token}'}).json()["id"]
    return str(user_id)


@pytest.fixture(scope="function")
def new_card(user_refresh_token):
    payload = new_card_payload()
    card_id = requests.post(URL.CARDS, headers={'Authorization': f'Bearer {user_refresh_token}'},
                            json=payload).json()["id"]
    yield {"id": str(card_id),
           "token": user_refresh_token}
    requests.delete(URL.CARDS + str(card_id) + "/", headers={'Authorization': f'Bearer {user_refresh_token}'})


@pytest.fixture(scope="function")
def active_card(new_card, admin_token):
    requests.post(URL.CARDS + new_card["id"] + "/change_status/", headers={'Authorization': f'Bearer {admin_token}'})
    return new_card


@pytest.fixture(scope="function")
def archive_card(active_card):
    requests.post(URL.CARDS + active_card["id"] + "/archive/",
                  headers={'Authorization': f'Bearer {active_card["token"]}'})
    return active_card


@pytest.fixture(scope="function")
def new_service(user_refresh_token):
    payload = new_service_card_payload()
    card_id = requests.post(URL.SERVICE_CARDS, headers={'Authorization': f'Bearer {user_refresh_token}'},
                            json=payload).json()["id"]
    yield {"id": str(card_id),
           "token": user_refresh_token}
    requests.delete(URL.CARDS + str(card_id) + "/", headers={'Authorization': f'Bearer {user_refresh_token}'})


@pytest.fixture(scope="function")
def active_service(new_service, admin_token):
    requests.post(URL.CARDS + new_service["id"] + "/change_status/",
                  headers={'Authorization': f'Bearer {admin_token}'})
    return new_service


@pytest.fixture(scope="function")
def archive_service(active_service):
    requests.post(URL.SERVICE_CARDS + active_service["id"] + "/archive/",
                  headers={'Authorization': f'Bearer {active_service["token"]}'})
    return active_service


@pytest.fixture(scope="function")
def create_dialog(active_card, user_token):
    return {
        "seller": active_card["token"],
        "id": int(active_card["id"]),
        "buyer": user_token,
    }


@pytest.fixture(scope="function")
def new_dialog(create_dialog):
    dialog_id = requests.post(URL.DIALOGS + "/create/",
                              headers={"Authorization": f"Bearer {create_dialog["buyer"]}"},
                              json={"card": create_dialog["id"]}).json()["id"]
    create_dialog["dialog_id"] = dialog_id
    return create_dialog


@pytest.fixture(scope="function")
def dialog(new_dialog):
    requests.post(URL.MESSAGE, headers={"Authorization": f"Bearer {new_dialog["buyer"]}"},
                  json={"text": "pu-pu-pu"})
    return new_dialog


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
