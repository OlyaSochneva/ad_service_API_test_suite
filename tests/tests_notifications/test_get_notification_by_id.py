import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from check_response import check_structure, return_id
from response_samples import Sample


class TestGetNotificationById:
    @allure.title('По запросу GET /api/notifications/{id} получаем уведомление c нужным id')
    def test_get_notification_by_id_success(self, notification):
        response = requests.get(URL.NOTIFICATIONS + str(notification["id"]),
                                headers={'Authorization': f'Bearer {notification["token"]}'})
        response_structure = check_structure(response.json(), Sample.NOTIFICATION_STRUCTURE)
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == notification["id"])

    @allure.title('Err.401, если не передать токен или передать невалидный')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_get_notification_by_id_unauthorized_causes_401_error(self, notification, wrong_headers, error_message):
        response = requests.get(URL.NOTIFICATIONS + str(notification["id"]), headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('Err.404 если передать неверный id уведомления (несуществующий или невалидный - буквы и тд)')
    @pytest.mark.parametrize('wrong_id, error_message', [
        ("66666", Message.NON_EXISTENT_NOTIFICATION),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_get_notification_by_wrong_id_causes_404_error(self, notification, wrong_id, error_message):
        response = requests.get(URL.NOTIFICATIONS + wrong_id,
                                headers={'Authorization': f'Bearer {notification["token"]}'})
        assert (response.status_code == 404 and error_message in str(response.json()))
