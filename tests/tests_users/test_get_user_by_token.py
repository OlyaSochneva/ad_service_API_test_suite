import allure
import pytest
import requests

from data import URL, Message
from response_samples import Sample
from check_response import check_structure
from assistant_methods import generate_random_string


class TestGetUserByToken:
    @allure.title('По запросу GET /api/users/me/  получаем ответ с корректной структурой')
    def test_get_authorized_user_by_token_success(self, user_token):
        response = requests.get(URL.USER_ME, headers={'Authorization': f'Bearer {user_token}'})
        response_structure = check_structure(response.json(), Sample.USER_STRUCTURE)
        assert (response.status_code == 200 and response_structure == "Correct")

    @allure.title('Err.401 если не передать токен или передать невалидный')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(15)}'}, Message.INVALID_TOKEN)
    ])
    def test_get_user_unauthorized_causes_error(self, wrong_headers, error_message):
        response = requests.get(URL.USER_ME, headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

