import allure
import pytest
import requests

from data import URL, Message
from response_samples import Sample
from check_response import check_structure, return_id


class TestGetUser:
    @allure.title('По запросу GET /api/users/{id} получаем нужного пользователя')
    def test_get_user_by_id_success(self, user_id):
        response = requests.get(URL.USERS + str(user_id), timeout=10)
        response_structure = check_structure(response.json(), Sample.USER_STRUCTURE)
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == user_id)

    @allure.title('Err.404 если передать неверный id пользователя (несуществующий или невалидный - буквы и тд)')
    @pytest.mark.parametrize('wrong_id, error_message', [
        ("66666", Message.NON_EXISTENT_USER),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_get_user_by_wrong_id_causes_404_error(self, wrong_id, error_message):
        response = requests.get(URL.USERS + wrong_id, timeout=10)
        assert (response.status_code == 404 and error_message in str(response.json()))
