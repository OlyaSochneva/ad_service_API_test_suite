import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from response_samples import Sample
from check_response import check_list_structure, check_structure


class TestGetNotifications:
    @allure.title('По запросу GET /api/notifications/ получаем список уведомлений пользователя с корректной структурой')
    def test_get_notifications_list_success(self, user_with_ntf_token):
        response = requests.get(URL.NOTIFICATIONS, headers={'Authorization': f'Bearer {user_with_ntf_token}'})
        #print(response.json())   # посмотреть id уведомления
        response_structure = check_list_structure(response.json(), check_structure, Sample.NOTIFICATION_STRUCTURE)
        assert (response.status_code == 200 and response_structure == "Correct")

    @allure.title('Err.401 если не передать токен или передать невалидный')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)
    ])
    def test_get_notifications_list_unauthorized_causes_401_error(self, wrong_headers, error_message):
        response = requests.get(URL.NOTIFICATIONS, headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

