import pytest
import allure
import requests

from data import URL, Message, TestData as Test
from response_samples import Sample
from check_response import check_structure, return_id


class TestGetCategoryById:
    @allure.title('По запросу GET /api/categories/{id} получаем категорию c нужным id')
    def test_get_category_by_id_success(self):
        response = requests.get(URL.CATEGORIES + str(Test.CATEGORY_ID), timeout=10)
        response_structure = check_structure(response.json(), Sample.CATEGORY_STRUCTURE)
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == Test.CATEGORY_ID)

    @allure.title('Err.404 если передать неверный id категории (несуществующий или невалидный - буквы и тд)')
    @pytest.mark.parametrize('wrong_id, error_message', [
        ("66666", Message.NON_EXISTENT_CATEGORY),
        ("pu-pu-@pu", Message.PAGE_NOT_FOUND)])
    def test_get_category_by_wrong_id_causes_404_error(self, wrong_id, error_message):
        response = requests.get(URL.CATEGORIES + wrong_id, timeout=10)
        assert (response.status_code == 404 and error_message in str(response.json()))


