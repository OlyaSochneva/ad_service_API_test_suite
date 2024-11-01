import allure
import pytest
import requests

from assistant_methods import generate_random_string, return_is_read
from data import URL, Message
from payloads import read_notification_payload, unread_notification_payload


class TestReadNotification:
    @allure.title('Можно поменять статус уведомления на прочитанное')
    @pytest.mark.order(1)
    def test_read_notification_success(self, notification):
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'},
                                  json=read_notification_payload())
        is_read = return_is_read(response.json())
        assert (response.status_code == 200 and is_read is True)

    @allure.title('Нельзя прочитать уведомление, которое уже прочитано')
    @pytest.mark.order(2)
    def test_read_notification_twice(self, notification):
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'},
                                  json=read_notification_payload())
        assert response.status_code == 400

    @allure.title('Можно поменять статус уведомления на непрочитанное')
    @pytest.mark.order(3)
    def test_unread_notification_success(self, notification):
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'},
                                  json=unread_notification_payload())
        is_read = return_is_read(response.json())
        assert (response.status_code == 200 and is_read is False)

    @allure.title('Нельзя поменять статус уведомления на непрочитанное, если оно уже непрочитанное')
    @pytest.mark.order(4)
    def test_unread_notification_twice(self, notification):
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'},
                                  json=unread_notification_payload())
        assert response.status_code == 400

    @allure.title('(401)Нельзя прочитать уведомление с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_read_notification_unauthorized_causes_error(self, notification, wrong_headers, error_message):
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers=wrong_headers,
                                  json=read_notification_payload())
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(404)Нельзя прочитать уведомление с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, error_message', [
        ("66666", Message.NON_EXISTENT_NOTIFICATION),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_read_notification_by_wrong_id_causes_404_error(self, notification, wrong_id, error_message):
        response = requests.patch(URL.NOTIFICATIONS + wrong_id + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'},
                                  json=read_notification_payload())
        assert (response.status_code == 404 and error_message in str(response.json()))

    @allure.title('(400)Нельзя прочитать уведомление, если не передать тело запроса')
    def test_read_notification_without_payload_causes_error(self, notification):
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'})
        assert (response.status_code == 400)

    @allure.title('(400)Нельзя прочитать уведомление, если передать неверное тело запроса (не булево значение)')
    @pytest.mark.parametrize('invalid_value, error_message', [
        ("pupupu", Message.MUST_BE_BOOLEAN),
        (15, Message.MUST_BE_BOOLEAN),
        (None, Message.EMPTY_FIELD)])
    def test_read_notification_with_invalid_payload_causes_error(self, notification, invalid_value, error_message):
        payload = {"is_read": invalid_value}
        response = requests.patch(URL.NOTIFICATIONS + str(notification["id"]) + "/",
                                  headers={'Authorization': f'Bearer {notification["token"]}'},
                                  json=payload)
        assert (response.status_code == 400 and error_message in str(response.json()))
