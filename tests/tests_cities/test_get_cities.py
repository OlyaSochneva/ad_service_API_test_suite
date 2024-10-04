import allure
import requests

from data import URL
from response_samples import Sample
from check_response import check_list_structure, check_item_structure


class TestGetCities:
    @allure.title('По запросу GET /api/cities/ получаем список городов с корректной структурой')
    def test_get_cities_list(self):
        response = requests.get(URL.CITIES, params={'limit': 10}, timeout=10)
        response_structure = check_list_structure(response.json(), check_item_structure, Sample.CITY_STRUCTURE)
        assert (response.status_code == 200 and response_structure == "Correct")
