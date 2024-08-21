import allure
import pytest
import requests

from data import URL, Message, TestData as Test
from response_samples import Sample
from check_response import check_response_structure as check_structure
from check_response import check_user, check_values


class TestGetUsers:
    @allure.title('Проверка: по запросу GET /api/users/ получаем список пользователей с корректной структурой')
    def test_get_users_list(self):
        response = requests.get(URL.USERS, params={'limit': 100}, timeout=10)
        response_structure = check_structure(response.json(), check_user, Sample.USER_STRUCTURE)
        assert (response.status_code == 200 and response_structure == "Correct")

    @allure.title('Проверка: по запросу GET /api/users/{id} получаем нужного пользователя, '
                  'значения всех полей совпадают с образцом')
    def test_get_user_by_id_success(self):
        user_id = str(Test.USER["id"])
        response = requests.get(URL.USERS + user_id, timeout=10)
        result = check_values(response.json(), Test.USER)
        assert response.status_code == 200 and result == "Correct"

    @allure.title('Проверка: если передать неверный id пользователя (несуществующий или невалидный - буквы и тд), '
                  'вернётся ошибка 404')
    @pytest.mark.parametrize('user_id, error_message', [
        ("666", Message.NON_EXISTENT_USER),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_get_user_by_wrong_id_causes_404_error(self, user_id, error_message):
        response = requests.get(URL.USERS + user_id, timeout=10)
        assert (response.status_code == 404 and
                error_message in str(response.json()))
