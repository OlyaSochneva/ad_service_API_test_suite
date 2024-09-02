import allure
import pytest
import requests

from assistant_methods import read_notification_payload, generate_random_string, unread_notification_payload
from data import URL, Message


class TestReadNotification:
    @allure.title('С корректными данными статус уведомления меняется на прочитанное/непрочитанное')
    @pytest.mark.parametrize('payload, read_status', [
        (read_notification_payload(), True),
        (unread_notification_payload(), False)])
    def test_change_read_status_success(self, new_notification_id_and_user_token, payload, read_status):
        user_ntf_id = new_notification_id_and_user_token["id"]
        token = new_notification_id_and_user_token["token"]
        response = requests.patch(URL.NOTIFICATIONS + str(user_ntf_id) + "/",
                                  headers={'Authorization': f'Bearer {token}'}, json=payload)
        assert (response.status_code == 200 and response.json().get("is_read") == read_status)

    @allure.title('Если не передать токен или передать невалидный, будет ошибка 401')
    @pytest.mark.parametrize('headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_read_notification_unauthorized_causes_error(self, new_notification_id_and_user_token,
                                                         headers, error_message):
        user_ntf_id = new_notification_id_and_user_token["id"]
        response = requests.patch(URL.NOTIFICATIONS + str(user_ntf_id) + "/", headers=headers,
                                  json=read_notification_payload())
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('Если передать неверный id уведомления (несуществующий или невалидный - буквы и тд), '
                  'вернётся ошибка 404')
    @pytest.mark.parametrize('notification_id, error_message', [
        ("66666", Message.NON_EXISTENT_NOTIFICATION),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_read_notification_by_wrong_id_causes_404_error(self, new_notification_id_and_user_token,
                                                            notification_id, error_message):
        token = new_notification_id_and_user_token["token"]
        response = requests.patch(URL.NOTIFICATIONS + notification_id + "/",
                                  headers={'Authorization': f'Bearer {token}'}, json=read_notification_payload())
        assert (response.status_code == 404 and error_message in str(response.json()))

    @allure.title('Если передать неверное тело запроса (не булево значение), вернется ошибка 400')
    @pytest.mark.parametrize('invalid_value', ["pupupu", 15, None])
    def test_read_notification_with_invalid_payload_causes_error(self, new_notification_id_and_user_token, invalid_value):
        user_ntf_id = new_notification_id_and_user_token["id"]
        token = new_notification_id_and_user_token["token"]
        payload = {"is_read": invalid_value}
        response = requests.patch(URL.NOTIFICATIONS + str(user_ntf_id) + "/",
                                  headers={'Authorization': f'Bearer {token}'}, json=payload)
        assert response.status_code == 400



