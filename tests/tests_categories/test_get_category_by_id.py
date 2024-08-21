import pytest
import allure
import requests

from data import URL, Message, TestData as Test
from check_response import check_id


class TestGetCategoryById:
    @allure.title('Проверка: по запросу GET /api/categories/{id} получаем категорию c правильным id')
    def test_get_category_by_id_success(self):
        response = requests.get(URL.CATEGORIES + str(Test.CATEGORY_ID), timeout=10)
        result = check_id(response.json(), Test.CATEGORY_ID)
        assert response.status_code == 200 and result == "Correct"

    @allure.title('Проверка: если передать неверный id категории (несуществующий или невалидный - буквы и тд), '
                  'вернётся ошибка 404')
    @pytest.mark.parametrize('category_id, error_message', [
        ("666", Message.NON_EXISTENT_CATEGORY),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_get_category_by_wrong_id_causes_404_error(self, category_id, error_message):
        response = requests.get(URL.CATEGORIES + category_id, timeout=10)
        assert (response.status_code == 404 and
                error_message in str(response.json()))
