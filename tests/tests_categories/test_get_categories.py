import allure
import pytest
import requests

from data import URL, Data
from response_samples import Sample
from check_response import check_list_structure
from check_response import check_category, check_categories_names, check_subcategories_names


class TestGetCategories:
    @allure.title('По запросу GET /api/categories/ получаем ответ с корректной структурой и правильным списком '
                  'всех категорий (проверяем по названиям)')
    def test_get_categories_list(self):
        response = requests.get(URL.CATEGORIES, params={'limit': 100}, timeout=10)
        response_structure = check_list_structure(response.json(), check_category, Sample.CATEGORY_STRUCTURE)
        assert (response.status_code == 200 and response_structure == "Correct")

    #@allure.title('По запросу GET /api/categories/ категориям 1 уровня соответствует правильный список '
                  #'подкатегорий (проверяем по названиям)')
    #@pytest.mark.parametrize("category_name, sample", [
        #("Транспорт", Data.TRANSPORT_SUBCATEGORIES),
        #("Услуги", Data.SERVICES_SUBCATEGORIES),
        #("Строительство", Data.CONSTRUCTION_SUBCATEGORIES)
    #])
    #def test_second_level_categories(self, category_name, sample):
        #response = requests.get(URL.CATEGORIES, params={'limit': 100}, timeout=10)
        #result = check_subcategories_names(response.json(), category_name, sample)
        #assert response.status_code == 200 and result == "Correct"

    #@allure.title('По запросу GET /api/categories/ категориям 2 уровня соответствует правильный список '
                  #'подкатегорий (проверяем по названиям)')
    #@pytest.mark.parametrize("category_name, sample", [
        #("Ремонт и обслуживание техники", Data.REPAIR_SERVICE_SUBCATEGORIES),
        #("Красота и здоровье", Data.BEAUTY_HEALTH_SUBCATEGORIES),
        #("Обучение и курсы", Data.STUDYING_SUBCATEGORIES),
        #("Аренда техники", Data.TRANSPORT_RENTAL_SUBCATEGORIES),
        #("Пассажирские перевозки", Data.TRANSPORTATION_SUBCATEGORIES)
    #])
    #def test_third_level_categories(self, category_name, sample):
        #response = requests.get(URL.CATEGORIES, params={'limit': 100}, timeout=10)
        #result = check_subcategories_names(response.json(), category_name, sample)
        #assert response.status_code == 200 and result == "Correct"



