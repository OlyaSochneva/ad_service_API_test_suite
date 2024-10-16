import allure
import pytest
import requests

from assistant_methods import generate_random_string
from payloads import notification_payload
from data import URL, Message
from response_samples import Sample
from check_response import check_structure


class TestCreateNotification:
    @allure.title('По запросу POST /api/notifications/ с корректными данными можно создать новое уведомление')
    def test_create_notification_for_one_user_success(self, admin_token, user_id, user_token):
        payload = notification_payload(user_id)
        response = requests.post(URL.NOTIFICATIONS,
                                 headers={'Authorization': f'Bearer {admin_token}'},
                                 json=payload)
        response_structure = check_structure(response.json(), Sample.NOTIFICATION_CREATED_STRUCTURE)
        assert (response.status_code == 201 and response_structure == "Correct")

    @allure.title('Нельзя создать уведомление c пользовательским токеном')
    def test_create_notification_with_user_token_causes_error(self, user_id, user_token):
        payload = notification_payload(user_id)
        response = requests.post(URL.NOTIFICATIONS,
                                 headers={'Authorization': f'Bearer {user_token}'},
                                 json=payload)
        assert (response.status_code == 403 and Message.NOT_SUFFICIENT_RIGHTS in str(response.json()))

    @allure.title('Нельзя создать уведомление, если не передать токен или передать невалидный')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN),
        (None, Message.CREDENTIALS_NOT_FOUND)
    ])
    def test_create_notification_unauthorized_causes_error(self, user_id, wrong_headers, error_message):
        payload = notification_payload(user_id)
        response = requests.post(URL.NOTIFICATIONS, headers=wrong_headers, json=payload)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('Нельзя создать уведомление, если список users пустой')
    def test_create_notification_without_users_causes_error(self, admin_token, user_id):
        payload = notification_payload(user_id)
        payload["users"] = []
        response = requests.post(URL.NOTIFICATIONS, headers={'Authorization': f'Bearer {admin_token}'},
                                 json=payload)
        assert response.status_code == 400 and Message.EMPTY_USERS_LIST

    @allure.title('Нельзя создать уведомление, если одно из обязательных полей отсутствует')
    @pytest.mark.parametrize('deleted_field', ["title", "description", "users"])
    def test_create_new_notification_without_required_field_causes_error(self, user_id, admin_token, deleted_field):
        payload = notification_payload(user_id)
        payload.pop(deleted_field)
        response = requests.post(URL.NOTIFICATIONS, headers={'Authorization': f'Bearer {admin_token}'},
                                 json=payload)
        #print(response.json())
        assert response.status_code == 400





