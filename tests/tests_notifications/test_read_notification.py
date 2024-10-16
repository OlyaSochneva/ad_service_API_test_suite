import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from payloads import read_notification_payload, unread_notification_payload


class TestReadNotification:
    @allure.title('С корректными данными статус уведомления меняется на прочитанное/непрочитанное')
    def test_change_read_status_success(self, notification):
        payload = read_notification_payload()
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'},
                                  json=payload)
        assert response.status_code == 200 #and response.json().get("is_read") == read_status)

    @allure.title('Если не передать токен или передать невалидный, будет ошибка 401')
    @pytest.mark.parametrize('headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_read_notification_unauthorized_causes_error(self, notification, headers, error_message):
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers=headers,
                                  json=read_notification_payload())
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('Err.404 если передать неверный id уведомления (несуществующий или невалидный - буквы и тд')
    @pytest.mark.parametrize('wrong_id, error_message', [
        ("66666", Message.NON_EXISTENT_NOTIFICATION),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_read_notification_by_wrong_id_causes_404_error(self, notification, wrong_id, error_message):
        response = requests.patch(URL.NOTIFICATIONS + wrong_id + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'},
                                  json=read_notification_payload())
        assert (response.status_code == 404 and error_message in str(response.json()))

    @allure.title('Err.400 если не передать тело запроса')
    def test_read_notification_without_payload_causes_error(self, notification):
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'})
        #print(response.json())
        assert (response.status_code == 400)

    @allure.title('Err.400 если передать неверное тело запроса (не булево значение)')
    @pytest.mark.parametrize('invalid_value, error_message', [
        ("pupupu", Message.MUST_BE_BOOLEAN),
        (15, Message.MUST_BE_BOOLEAN),
        (None, Message.EMPTY_FIELD)])
    def test_read_notification_with_invalid_payload_causes_error(self, notification, invalid_value, error_message):
        payload = {"is_read": invalid_value}
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'},
                                  json=payload)
        #print(response.json())
        assert (response.status_code == 400 and error_message in str(response.json()))


