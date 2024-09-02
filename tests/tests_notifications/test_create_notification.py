import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message, TestData as Test
from response_samples import Sample
from check_response import check_item_structure


class TestCreateNotification:
    @allure.title('По запросу POST /api/notifications/ с корректными данными можно создать новое уведомление')
    def test_create_notification_for_one_user_success(self, new_notification_payload):
        #print(admin_token)
        payload = new_notification_payload
        response = requests.post(URL.NOTIFICATIONS,
                                 headers={'Authorization': f'Bearer {Test.ADMIN_TOKEN}'},
                                 json=payload)
        print(response.json())
        response_structure = check_item_structure(response.json(), Sample.NOTIFICATION_CREATED_STRUCTURE)
        assert (response.status_code == 201 and response_structure == "Correct")

    @allure.title('Нельзя создать уведомление c пользовательским токеном')
    def test_create_notification_with_user_token_causes_error(self, new_user_id_and_token,
                                                              new_notification_payload):
        response = requests.post(URL.NOTIFICATIONS,
                                 headers={'Authorization': f'Bearer {new_user_id_and_token["token"]}'},
                                 json=new_notification_payload)
        assert (response.status_code == 403 and Message.NOT_SUFFICIENT_RIGHTS in str(response.json()))

    @allure.title('Нельзя создать уведомление, если не передать токен или передать невалидный')
    @pytest.mark.parametrize('headers, error_message', [
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN),
        (None, Message.CREDENTIALS_NOT_FOUND)
    ])
    def test_create_notification_unauthorized_causes_error(self, new_notification_payload,
                                                           headers, error_message):
        payload = new_notification_payload
        response = requests.post(URL.NOTIFICATIONS, headers=headers, json=payload)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('POST /api/notifications/ если одно из обязательных полей отсутствует, вернётся ошибка 401')
    @pytest.mark.parametrize('deleted_field', ["title", "description", "users"])
    def test_create_new_notification_without_required_field_causes_error(self, new_notification_payload, deleted_field):
        payload = new_notification_payload
        payload.pop(deleted_field)
        response = requests.post(URL.NOTIFICATIONS, headers={'Authorization': f'Bearer {Test.ADMIN_TOKEN}'},
                                 json=payload)
        assert response.status_code == 401





