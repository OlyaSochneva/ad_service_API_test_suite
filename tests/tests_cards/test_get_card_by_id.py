import allure
import pytest
import requests

from data import URL, Message, TestData as Test
from check_response import check_id


class TestGetCardById:
    @allure.title('Проверка: по запросам GET/api/cards/{id}, GET/api/cards/services{id} и GET/api/cards/vehicles/{id}'
                  'получаем карточку с правильным id')
    @pytest.mark.parametrize('test_id, type_of_request', [
        (Test.CARD_ID, URL.CARDS),
        (Test.SERVICE_CARD_ID, URL.SERVICES),
        (Test.VEHICLE_CARD_ID, URL.VEHICLES)])
    def test_get_card_by_id_success(self, test_id, type_of_request):
        response = requests.get(type_of_request + str(test_id), timeout=10)
        result = check_id(response.json(), test_id)
        assert response.status_code == 200 and result == "Correct"

    @allure.title('Проверка: если передать несуществующий id карточки (обычной/услуг/транспорта), '
                  'вернётся ошибка 404')
    @pytest.mark.parametrize('type_of_request, error_message', [
        (URL.CARDS, Message.NON_EXISTENT_CARD),
        (URL.SERVICES, Message.NON_EXISTENT_SERVICE_CARD),
        (URL.VEHICLES, Message.NON_EXISTENT_VEHICLE_CARD)])
    def test_get_card_by_non_existent_id_causes_404_error(self, type_of_request, error_message):
        response = requests.get(type_of_request + "666", timeout=10)
        assert (response.status_code == 404 and error_message in str(response.json()))

    @allure.title('Проверка: если передать невалидный (буквы и тд) id карточки (обычной/услуг/транспорта), '
                  'вернётся ошибка 404')
    @pytest.mark.parametrize('type_of_request', [URL.CARDS, URL.SERVICES, URL.VEHICLES])
    def test_get_card_by_invalid_id_causes_404_error(self, type_of_request):
        response = requests.get(type_of_request + "pu-pu-pu", timeout=10)
        assert (response.status_code == 404 and
                Message.PAGE_NOT_FOUND in str(response.json()))

    @allure.title('Проверка: если запросить карточку по id, она не попадает на модерацию (не пропадает из выдачи)')
    def test_get_card_by_id_twice_does_not_change_status_to_moderation(self):
        card_id = str(Test.CARD_ID)
        response_1 = requests.get(URL.CARDS + card_id, timeout=10)
        response_2 = requests.get(URL.CARDS + card_id, timeout=10)
        assert (response_1.status_code == 200 and response_2.status_code == 200)
