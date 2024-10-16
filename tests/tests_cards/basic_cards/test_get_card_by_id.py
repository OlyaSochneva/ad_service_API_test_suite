import allure
import pytest
import requests

from data import URL, Message
from response_samples import Sample
from check_response import check_structure, return_id


class TestGetCardById:
    @allure.title('По запросу GET/api/cards/{id} получаем карточку с нужным id')
    def test_get_card_by_id_success(self, basic_card):
        response = requests.get(URL.CARDS + str(basic_card["id"]) + "/")
        response_structure = check_structure(response.json(), Sample.CARD_STRUCTURE)
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == basic_card["id"])

    @allure.title('Err.404/400, если передать неверный id карточки (несуществующий и невалидный - буквы и тд)')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_get_card_by_incorrect_id_causes_error(self, wrong_id, status_code, error_message):
        response = requests.get(URL.CARDS + wrong_id, timeout=10)
        assert (response.status_code == status_code and error_message in str(response.json()))


    #@allure.title('Проверка: если запросить карточку по id, она не попадает на модерацию (не пропадает из выдачи)')
    #def test_get_card_by_id_twice_does_not_change_status_to_moderation(self):
        #card_id = str(Test.CARD_ID)
        #response_1 = requests.get(URL.CARDS + card_id, timeout=10)
        #response_2 = requests.get(URL.CARDS + card_id, timeout=10)
        #assert (response_1.status_code == 200 and response_2.status_code == 200)
