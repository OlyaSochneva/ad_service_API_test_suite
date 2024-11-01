import allure
import pytest
import requests

from data import URL, Message
from response_samples import Sample
from check_response import check_structure, return_id


class TestGetCardById:
    @allure.title('Можно получить нужную карточку по id')
    def test_get_card_by_id_success(self, basic_card):
        response = requests.get(URL.CARDS + str(basic_card["id"]) + "/")
        response_structure = check_structure(response.json(), Sample.CARD_STRUCTURE)
        response_id = return_id(response.json())
        assert (response.status_code == 200 and
                response_structure == "Correct" and
                response_id == basic_card["id"])

    @allure.title('(404/400)Нельзя получить карточку с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_get_card_by_incorrect_id_causes_error(self, wrong_id, status_code, error_message):
        response = requests.get(URL.CARDS + wrong_id, timeout=10)
        assert (response.status_code == status_code and error_message in str(response.json()))

    class TestGetServiceCardById:
        @allure.title('Можно получить нужную карточку услуг по id')
        def test_get_service_card_by_id_success(self, service_card):
            response = requests.get(URL.SERVICE_CARDS + str(service_card["id"]) + "/")
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

        # @allure.title('Проверка: если запросить карточку по id, она не попадает на модерацию (не пропадает из выдачи)')
        # def test_get_card_by_id_twice_does_not_change_status_to_moderation(self):
        # card_id = str(Test.CARD_ID)
        # response_1 = requests.get(URL.CARDS + card_id, timeout=10)
        # response_2 = requests.get(URL.CARDS + card_id, timeout=10)
        # assert (response_1.status_code == 200 and response_2.status_code == 200)
