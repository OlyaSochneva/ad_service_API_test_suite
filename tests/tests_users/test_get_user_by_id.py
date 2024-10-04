import allure
import pytest
import requests

from data import URL, Message
from check_response import check_id


class TestGetUser:
    @allure.title('По запросу GET /api/users/{id} получаем нужного пользователя')
    def test_get_user_by_id_success(self, new_user_id_and_token):
        user_id = new_user_id_and_token["id"]
        response = requests.get(URL.USERS + str(user_id), timeout=10)
        result = check_id(response.json(), user_id)
        assert response.status_code == 200 and result == "Correct"

    @allure.title('Если по запросу GET /api/users/{id} передать неверный id пользователя '
                  '(несуществующий или невалидный - буквы и тд), вернётся ошибка 404')
    @pytest.mark.parametrize('user_id, error_message', [
        ("66666", Message.NON_EXISTENT_USER),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_get_user_by_wrong_id_causes_404_error(self, user_id, error_message):
        response = requests.get(URL.USERS + user_id, timeout=10)
        assert (response.status_code == 404 and error_message in str(response.json()))




