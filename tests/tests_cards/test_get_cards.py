import allure
import requests

from data import URL
from response_samples import Sample
from check_response import check_response_structure as check_structure
from check_response import check_card, check_cards_category


class TestGetCards:
    @allure.title('Проверка: по запросу GET /api/cards/ получаем ответ с корректной структурой')
    def test_get_cards_list(self):
        response = requests.get(URL.CARDS, params={'limit': 100}, timeout=10)
        response_structure = check_structure(response.json(), check_card, Sample.CARD_STRUCTURE)
        # print(f"Response structure: '{response_structure}'")
        assert (response.status_code == 200 and response_structure == "Correct")

    @allure.title('Проверка: по запросу GET /api/cards/services получаем ответ с корректной структурой '
                  'и правильным списком карточек (все карточки относятся к услугам)')
    def test_get_services_cards_list(self):
        response = requests.get(URL.SERVICES, params={'limit': 100}, timeout=10)
        response_structure = check_structure(response.json(), check_card, Sample.SERVICE_CARD_STRUCTURE)
        cards_category = check_cards_category(response.json(), "Услуги")
        assert (response.status_code == 200
                and response_structure == "Correct"
                and cards_category == "Correct")

    @allure.title('Проверка: по запросу GET /api/cards/vehicles получаем ответ с корректной структурой '
                  'и правильным списком карточек (все карточки относятся к транспорту)')
    def test_get_vehicles_cards_list(self):
        response = requests.get(URL.VEHICLES, params={'limit': 100}, timeout=10)
        response_structure = check_structure(response.json(), check_card, Sample.VEHICLE_CARD_STRUCTURE)
        cards_category = check_cards_category(response.json(), "Легковые авто")
        assert (response.status_code == 200
                and response_structure == "Correct"
                and cards_category == "Correct")
