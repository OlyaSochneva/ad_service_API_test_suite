import allure
import pytest
import requests

from data import URL, Message
from response_samples import Sample
from check_response import check_structure, return_id


class TestGetServiceCardById:
    @allure.title('По запросу GET/api/cards/services/{id} получаем карточку услуги с нужным id')
    def test_get_service_card_by_id_success(self, new_service_card_id_and_token):
        card_id = new_service_card_id_and_token["card_id"]
        response = requests.get(URL.SERVICE_CARDS + str(card_id))
        response_structure = check_structure(response.json(), Sample.SERVICE_CARD_STRUCTURE)
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == card_id)

    @allure.title('Ошибка если передать неверный id карточки услуги (несуществующий или невалидный - буквы и тд)')
    @pytest.mark.parametrize('card_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_SERVICE_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_get_service_card_by_incorrect_id_causes_error(self, card_id, status_code, error_message):
        response = requests.get(URL.SERVICE_CARDS + card_id, timeout=10)
        assert (response.status_code == status_code and error_message in str(response.json()))