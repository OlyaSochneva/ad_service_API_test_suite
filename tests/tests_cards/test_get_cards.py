import allure
import pytest
import requests

from data import URL
from response_samples import Sample
from check_response import check_list_structure
from check_response import check_card, check_cards_category


class TestGetCards:
    @allure.title('GET /api/cards/ + services/vehicles получаем список карточек с корректной структурой')
    @pytest.mark.parametrize('type_of_request, card_sample', [
        (URL.CARDS, Sample.CARD_STRUCTURE),
        (URL.SERVICES, Sample.SERVICE_CARD_STRUCTURE),
        (URL.VEHICLES, Sample.VEHICLE_CARD_STRUCTURE)])
    def test_get_special_cards_list(self, type_of_request, card_sample):
        response = requests.get(type_of_request, params={'limit': 100}, timeout=10)
        response_structure = check_list_structure(response.json(), check_card, card_sample)
        assert (response.status_code == 200 and response_structure == "Correct")


