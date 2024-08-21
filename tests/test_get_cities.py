import allure
import pytest
import requests

from data import URL, Message, TestData as Test
from response_samples import Sample
from check_response import check_response_structure as check_structure
from check_response import check_city, check_values


class TestGetCities:
    @allure.title('Проверка: по запросу GET /api/cities/ получаем список городов с корректной структурой')
    def test_get_cities_list(self):
        response = requests.get(URL.CITIES, params={'limit': 10}, timeout=10)
        response_structure = check_structure(response.json(), check_city, Sample.CITY_STRUCTURE)
        assert (response.status_code == 200 and response_structure == "Correct")

    @allure.title('Проверка: по запросу GET /api/cities/{id} получаем правильный город, '
                  'значение всех полей совпадают с образцом')
    def test_get_city_by_id_success(self):
        city_id = str(Test.CITY["id"])
        response = requests.get(URL.CITIES + city_id, timeout=10)
        result = check_values(response.json(), Test.CITY)
        assert response.status_code == 200 and result == "Correct"

    @allure.title('Проверка: если передать неверный id города (несуществующий или невалидный - буквы и тд), '
                  'вернётся ошибка 404')
    @pytest.mark.parametrize('city_id, error_message', [
        ("66666", Message.NON_EXISTENT_CITY),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_get_city_by_wrong_id_causes_404_error(self, city_id, error_message):
        response = requests.get(URL.CITIES + city_id, timeout=10)
        assert (response.status_code == 404 and
                error_message in str(response.json()))
