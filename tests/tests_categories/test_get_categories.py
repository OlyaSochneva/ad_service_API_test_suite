import allure
import requests

from data import URL, Data
from response_samples import Sample
from check_response import check_response_structure as check_structure
from check_response import check_category, check_categories_names, check_subcategories_names


class TestGetCategories:
    @allure.title('Проверка: по запросу GET /api/categories/ получаем ответ с корректной структурой и '
                  'правильным списком категорий')
    def test_get_categories_list(self):
        response = requests.get(URL.CATEGORIES, params={'limit': 100}, timeout=10)
        response_structure = check_structure(response.json(), check_category, Sample.CATEGORY_STRUCTURE)
        #categories_list = check_categories_names(response.json())
        #print(f"Categories list: '{categories_list}'")
        assert (response.status_code == 200 and
                response_structure == "Correct")
                #and categories_list == "Correct")

    @allure.title('Проверка: по запросу GET /api/categories/ у категории "Услуги" приходит '
                  'правильный список подкатегорий')
    def test_services_subcategories(self):
        response = requests.get(URL.CATEGORIES, params={'limit': 100}, timeout=10)
        result = check_subcategories_names(response.json(), "Услуги", Data.SUBCATEGORIES_SERVICES)
        assert response.status_code == 200 and result == "Correct"

    @allure.title('Проверка: по запросу GET /api/categories/ у категории "Транспорт" приходит '
                  'правильный список подкатегорий')
    def test_transport_subcategories(self):
        response = requests.get(URL.CATEGORIES, params={'limit': 100}, timeout=10)
        result = check_subcategories_names(response.json(), "Транспорт", Data.SUBCATEGORIES_TRANSPORT)
        assert response.status_code == 200 and result == "Correct"

    @allure.title('Проверка: по запросу GET /api/categories/ у категории "Строительство" приходит '
                  'правильный список подкатегорий')
    def test_construction_subcategories(self):
        response = requests.get(URL.CATEGORIES, params={'limit': 100}, timeout=10)
        result = check_subcategories_names(response.json(), "Строительство", Data.SUBCATEGORIES_CONSTRUCTION)
        assert response.status_code == 200 and result == "Correct"
