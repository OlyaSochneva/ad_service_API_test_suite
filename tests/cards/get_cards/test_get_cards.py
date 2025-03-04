import allure
import requests

from admin_data import URL
from response_samples import Sample
from check_response import check_list_structure
from check_response import check_card


class TestGetCards:
    @allure.title('Получаем список карточек с корректной структурой')
    def test_get_cards_list(self):
        response = requests.get(URL.CARDS, params={'limit': 100}, timeout=10)
        response_structure = check_list_structure(response.json(), check_card, Sample.CARD_STRUCTURE)
        print(response.json())
        assert (response.status_code == 200 and response_structure == "Correct")

    @allure.title('Получаем список карточек услуг с корректной структурой')
    def test_get_service_cards_list(self):
        response = requests.get(URL.SERVICE_CARDS, params={'limit': 100}, timeout=10)
        response_structure = check_list_structure(response.json(), check_card, Sample.SERVICE_CARD_STRUCTURE)
        assert (response.status_code == 200 and response_structure == "Correct")
