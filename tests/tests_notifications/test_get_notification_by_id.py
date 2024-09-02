import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from check_response import check_id


class TestGetNotificationById:
    @allure.title('По запросу GET /api/notifications/{id} получаем уведомление c нужным id')
    def test_get_notification_by_id_success(self, new_notification_id_and_user_token):
        token = new_notification_id_and_user_token["token"]
        print(token)
        user_ntf_id = new_notification_id_and_user_token["id"]
        print(user_ntf_id)
        response = requests.get(URL.NOTIFICATIONS + str(user_ntf_id), headers={'Authorization': f'Bearer {token}'})
        result = check_id(response.json(), user_ntf_id)
        assert (response.status_code == 200 and result == "Correct")

    @allure.title('Если по запросу GET /api/notifications/{id} не передать токен или передать невалидный, '
                  'будет ошибка 401')
    @pytest.mark.parametrize('headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_get_notification_by_id_unauthorized_causes_401_error(self, new_notification_id_and_user_token,
                                                                  headers, error_message):
        user_ntf_id = new_notification_id_and_user_token["id"]
        response = requests.get(URL.NOTIFICATIONS + str(user_ntf_id), headers=headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('Если по запросу GET /api/notifications/{id} передать неверный id уведомления '
                  '(несуществующий или невалидный - буквы и тд), вернётся ошибка 404')
    @pytest.mark.parametrize('notification_id, error_message', [
        ("66666", Message.NON_EXISTENT_NOTIFICATION),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_get_notification_by_wrong_id_causes_404_error(self, new_notification_id_and_user_token,
                                                           notification_id, error_message):
        token = new_notification_id_and_user_token["token"]
        response = requests.get(URL.NOTIFICATIONS + notification_id, headers={'Authorization': f'Bearer {token}'})
        assert (response.status_code == 404 and error_message in str(response.json()))
