import allure
import pytest
import requests

from assistant_methods import return_card_status, generate_random_string
from data import URL, Message


class TestActivateCard:
    @allure.title('Пользователь может активировать свою карточку')
    def test_activate_card_by_user_success(self, archive_card):
        response = requests.post(URL.CARDS + archive_card["id"] + "/active/",
                                 headers={'Authorization': f'Bearer {archive_card["token"]}'})
        status = return_card_status(response.json())
        assert (response.status_code == 200 and status == "active")

    @allure.title('(404)Пользователь не может активировать свою карточку, если она уже активна')
    def test_activate_card_twice_by_user_causes_error(self, active_card):
        response = requests.post(URL.CARDS + active_card["id"] + "/active/",
                                 headers={'Authorization': f'Bearer {active_card["token"]}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ARCHIVE in str(response.json()))

    @allure.title('(401)Нельзя активировать карточку с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_activate_card_unauthorized_causes_error(self, wrong_headers, error_message, archive_card):
        response = requests.post(URL.CARDS + archive_card["id"] + "/active/", headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(404/400)Пользователь не может активировать карточку с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_activate_incorrect_id_card_by_user_causes_error(self, wrong_id, status_code, error_message, user_token):
        response = requests.post(URL.CARDS + wrong_id + "/active/", headers={'Authorization': f'Bearer {user_token}'})
        assert (response.status_code == status_code and error_message in str(response.json()))
