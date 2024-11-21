import allure
import pytest
import requests

from data import URL, Message
from response_samples import Sample
from check_response import check_structure, return_id


class TestGetServiceCardById:
    @allure.title('Можно получить нужную карточку услуг по id')
    def test_get_service_card_by_id_success(self, service_card):
        response = requests.get(URL.SERVICE_CARDS + service_card["id"] + "/")
        response_structure = check_structure(response.json(), Sample.SERVICE_CARD_STRUCTURE)
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == service_card["id"])

    @allure.title('(404/400)Нельзя получить карточку услуг с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_SERVICE_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_get_service_card_by_incorrect_id_causes_error(self, wrong_id, status_code, error_message):
        response = requests.get(URL.SERVICE_CARDS + wrong_id + "/", timeout=10)
        assert (response.status_code == status_code and error_message in str(response.json()))
