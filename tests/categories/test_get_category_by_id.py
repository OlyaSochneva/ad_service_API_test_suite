import pytest
import allure
import requests

from data import URL, Message, CATEGORY
from response_samples import Sample
from check_response import check_structure, return_id


#                                        GET /api/categories/{id}
class TestGetCategoryById:
    @allure.title('По запросу GET /api/categories/{id} получаем категорию c нужным id')
    @pytest.mark.parametrize('category_id', [
        CATEGORY.MAIN["Транспорт"],
        CATEGORY.MAIN["Услуги"],
        CATEGORY.MAIN["Недвижимость"],
        CATEGORY.MAIN["Строительство"],
        CATEGORY.MAIN["Личные вещи"],
        CATEGORY.MAIN["Товары для дома"],
        CATEGORY.MAIN["Всё для сада"],
        CATEGORY.MAIN["Электроника и бытовая техника"],
        CATEGORY.MAIN["Животные"],
        CATEGORY.MAIN["Оборудование и запчасти"]
    ])
    def test_get_category_by_id(self, category_id):
        response = requests.get(URL.CATEGORIES + category_id + "/", timeout=10)
        response_structure = check_structure(response.json(), Sample.CATEGORY_STRUCTURE)
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == category_id)

    @allure.title('(404)Нельзя получить категорию с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, error_message', [
        ("66666", Message.NON_EXISTENT_CATEGORY),
        ("pu-pu-@pu", Message.PAGE_NOT_FOUND)])
    def test_get_category_by_wrong_id_causes_404_error(self, wrong_id, error_message):
        response = requests.get(URL.CATEGORIES + wrong_id, timeout=10)
        assert (response.status_code == 404 and error_message in str(response.json()))
