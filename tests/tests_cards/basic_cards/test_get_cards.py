import allure
import requests

from data import URL
from response_samples import Sample
from check_response import check_list_structure
from check_response import check_card


class TestGetCards:
    @allure.title('GET /api/cards/ получаем список карточек с корректной структурой')
    def test_get_cards_list(self):
        response = requests.get(URL.CARDS, params={'limit': 100}, timeout=10)
        print(response.json())
        response_structure = check_list_structure(response.json(), check_card, Sample.CARD_STRUCTURE)
        assert (response.status_code == 200 and response_structure == "Correct")
