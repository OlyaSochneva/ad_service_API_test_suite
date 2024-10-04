import allure
import pytest
import requests

from data import URL, Message, TestData as Test
from check_response import check_values


class TestGetCityById:
    @allure.title('По запросу GET /api/cities/{id} получаем правильный город, значение всех полей совпадают с образцом')
    def test_get_city_by_id_success(self):
        city_id = str(Test.CITY["id"])
        response = requests.get(URL.CITIES + city_id, timeout=10)
        result = check_values(response.json(), Test.CITY)
        assert response.status_code == 200 and result == "Correct"

    @allure.title('Если передать неверный id города (несуществующий или невалидный - буквы и тд), '
                  'вернётся ошибка 404')
    @pytest.mark.parametrize('city_id, error_message', [
        ("66666", Message.NON_EXISTENT_CITY),
        ("pu-pu-pu", Message.PAGE_NOT_FOUND)])
    def test_get_city_by_wrong_id_causes_404_error(self, city_id, error_message):
        response = requests.get(URL.CITIES + city_id, timeout=10)
        assert (response.status_code == 404 and error_message in str(response.json()))
