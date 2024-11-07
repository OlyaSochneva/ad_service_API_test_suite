import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from check_response import check_structure, return_id
from response_samples import Sample


#                                          GET /api/notifications/{id}
class TestGetNotificationById:
    @allure.title('Можно получить нужное уведомление по id')
    def test_get_notification_by_id_success(self, notification):
        response = requests.get(URL.NOTIFICATIONS + str(notification["id"]),
                                headers={'Authorization': f'Bearer {notification["token"]}'})
        response_structure = check_structure(response.json(), Sample.NOTIFICATION_STRUCTURE)
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == notification["id"])

    @allure.title('(401)Нельзя получить уведомление с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_get_notification_by_id_unauthorized_causes_401_error(self, notification, wrong_headers, error_message):
        response = requests.get(URL.NOTIFICATIONS + str(notification["id"]), headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(404)Нельзя получить уведомление с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, error_message', [
        ("66666", Message.NON_EXISTENT_NOTIFICATION),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_get_notification_by_wrong_id_causes_404_error(self, notification, wrong_id, error_message):
        response = requests.get(URL.NOTIFICATIONS + wrong_id,
                                headers={'Authorization': f'Bearer {notification["token"]}'})
        assert (response.status_code == 404 and error_message in str(response.json()))
