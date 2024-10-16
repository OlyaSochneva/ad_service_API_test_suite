import allure
import pytest
import requests

from data import URL, Message, TestData as Test
from response_samples import Sample
from check_response import check_structure, return_id


class TestGetCityById:
    @allure.title('По запросу GET /api/cities/{id} получаем правильный город')
    def test_get_city_by_id_success(self):
        response = requests.get(URL.CITIES + str(Test.CITY_ID), timeout=10)
        response_structure = check_structure(response.json(), Sample.CITY_STRUCTURE)
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == Test.CITY_ID)

    @allure.title('Err.404 если передать неверный id города (несуществующий или невалидный - буквы и тд)')
    @pytest.mark.parametrize('wrong_id, error_message', [
        ("66666", Message.NON_EXISTENT_CITY),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_get_city_by_wrong_id_causes_404_error(self, wrong_id, error_message):
        response = requests.get(URL.CITIES + wrong_id, timeout=10)
        assert (response.status_code == 404 and error_message in str(response.json()))
