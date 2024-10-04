import allure
import pytest
import requests

from data import URL, Message
from check_response import check_id


class TestGetCardById:
    @allure.title('По запросу GET/api/cards/{id} получаем карточку с нужным id')
    def test_get_card_by_id_success(self, new_card_id_and_token):
        card_id = new_card_id_and_token["card_id"]
        response = requests.get(URL.CARDS + str(card_id))
        result = check_id(response.json(), card_id)
        assert (response.status_code == 200 and result == "Correct")

    @allure.title('Если передать неверный id карточки (несуществующий или невалидный - буквы и тд), вернётся ошибка')
    @pytest.mark.parametrize('card_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_get_card_by_incorrect_id_causes_error(self, card_id, status_code, error_message):
        response = requests.get(URL.CARDS + card_id, timeout=10)
        assert (response.status_code == status_code and error_message in str(response.json()))

    #@allure.title('Проверка: если запросить карточку по id, она не попадает на модерацию (не пропадает из выдачи)')
    #def test_get_card_by_id_twice_does_not_change_status_to_moderation(self):
        #card_id = str(Test.CARD_ID)
        #response_1 = requests.get(URL.CARDS + card_id, timeout=10)
        #response_2 = requests.get(URL.CARDS + card_id, timeout=10)
        #assert (response_1.status_code == 200 and response_2.status_code == 200)
