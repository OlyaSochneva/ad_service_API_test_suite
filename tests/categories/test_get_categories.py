import allure
import requests

from admin_data import URL
from response_samples import Sample
from check_response import check_list_structure, check_structure


class TestGetCategories:
    @allure.title('Получаем список категорий с корректной структурой')
    def test_get_categories_list(self):
        response = requests.get(URL.CATEGORIES, params={'limit': 200}, timeout=10)
        response_structure = check_list_structure(response.json(), check_structure, Sample.CATEGORY_STRUCTURE)
        print(response.json())
        assert (response.status_code == 200 and response_structure == "Correct")
















