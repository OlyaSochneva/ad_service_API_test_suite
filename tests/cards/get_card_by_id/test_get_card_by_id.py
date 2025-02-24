import allure
import pytest
import requests

from data import Message
from admin_data import URL
from response_samples import Sample
from check_response import check_structure, return_id


class TestGetCardById:
    @allure.title('Можно получить нужную карточку по id')
    def test_get_card_by_id_success(self, active_card):
        response = requests.get(URL.CARDS + active_card["id"] + "/")
        response_structure = check_structure(response.json(), Sample.CARD_STRUCTURE)
        print(response.json())
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == active_card["id"])

    @allure.title('(404/400)Нельзя получить карточку с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_get_card_by_incorrect_id_causes_error(self, wrong_id, status_code, error_message):
        response = requests.get(URL.CARDS + wrong_id, timeout=10)
        assert (response.status_code == status_code and error_message in str(response.json()))

