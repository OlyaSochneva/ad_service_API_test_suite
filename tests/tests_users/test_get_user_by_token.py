import allure
import pytest
import requests

from data import URL, Message
from response_samples import Sample
from check_response import check_item_structure
from assistant_methods import generate_random_string


class TestGetUserByToken:
    @allure.title('По запросу GET /api/users/me/  получаем ответ с корректной структурой')
    def test_get_authorized_user_by_token_success(self, new_user_id_and_token):
        token = new_user_id_and_token["token"]
        response = requests.get(URL.USER_ME, headers={'Authorization': f'Bearer {token}'})
        response_structure = check_item_structure(response.json(), Sample.USER_STRUCTURE)
        assert (response.status_code == 200 and response_structure == "Correct")

    @allure.title('Если не передать токен или передать невалидный, будет ошибка 401')
    @pytest.mark.parametrize('headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)
    ])
    def test_get_user_unauthorized_causes_error(self, headers, error_message):
        response = requests.get(URL.USER_ME, headers=headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

