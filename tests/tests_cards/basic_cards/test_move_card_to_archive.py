import allure
import pytest
import requests

from assistant_methods import return_card_status, generate_random_string, return_admin_token
from data import URL, Message, TestData as Test


class TestMoveCardToArchive:
    def test_move_card_to_archive_by_user_success(self):
        #print(new_card_id_and_token)
        card_id = 100
        token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyODE1NjI3OSw"
                 "iaWF0IjoxNzI4MDY5ODc5LCJqdGkiOiIwODU0NmQwMWExMmU0ZmQzOGMzNDMzYTNiYTYyMjU3MSIsImlkIjoyMzZ9."
                 "vSOLB3IOffTeVjy92LCZgPTcwNxmtPkOFvX1kNAQTts")
        requests.post(URL.CARDS + str(card_id) + "/active/",  # /active/  # /archive/
                      headers={'Authorization': f'Bearer {token}'})
        response = requests.post(URL.CARDS + str(card_id) + "/archive/",  # /active/  # /archive/
                                 headers={'Authorization': f'Bearer {token}'})
        status = return_card_status(response.json())
        assert response.status_code == 200 and status == "archive"

    def test_move_card_to_archive_by_admin_success(self):
        # print(return_admin_token())
        card_id = 100
        requests.post(URL.CARDS + str(card_id) + "/active/", headers={'Authorization': f'Bearer {Test.ADMIN_TOKEN}'})
        response = requests.post(URL.CARDS + str(card_id) + "/archive/",
                                 headers={'Authorization': f'Bearer {Test.ADMIN_TOKEN}'})
        status = return_card_status(response.json())
        assert response.status_code == 200 and status == "archive"

    @allure.title('Если не передать токен или передать невалидный, будет ошибка 401')
    @pytest.mark.parametrize('headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_move_card_to_archive_unauthorized_causes_401_error(self, headers, error_message):
        card_id = 85
        response = requests.post(URL.CARDS + str(card_id) + "/archive/", headers=headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('Если передать неверный id карточки (несуществующий или невалидный - буквы и тд), вернётся ошибка')
    @pytest.mark.parametrize('card_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_move_card_to_archive_by_incorrect_id_causes_error(self, card_id, status_code, error_message):
        response = requests.post(URL.CARDS + card_id + "/archive/",  # /active/  # /archive/
                                 headers={'Authorization': f'Bearer {Test.ADMIN_TOKEN}'})
        assert (response.status_code == status_code and error_message in str(response.json()))
