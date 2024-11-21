import allure
import pytest
import requests

from assistant_methods import return_card_status, generate_random_string
from data import URL, Message


class TestArchiveCard:

    @allure.title('Пользователь может перевести свою карточку в архив')
    def test_archive_card_by_user_success(self, active_card):
        response = requests.post(URL.CARDS + active_card["id"] + "/archive/",
                                 headers={'Authorization': f'Bearer {active_card["token"]}'})
        status = return_card_status(response.json())
        assert response.status_code == 200 and status == "archive"

    @allure.title('(404)Пользователь не может архивировать свою карточку, если она уже в архиве')
    def test_archive_card_twice_by_user_causes_error(self, archive_card):
        response = requests.post(URL.CARDS + archive_card["id"] + "/archive/",
                                 headers={'Authorization': f'Bearer {archive_card["token"]}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ACTIVE in str(response.json()))

    @allure.title('(401)Нельзя архивировать карточку с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_archive_card_unauthorized_causes_error(self, wrong_headers, error_message, active_card):
        response = requests.post(URL.CARDS + active_card["id"] + "/archive/", headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(404/400)Пользователь не может архивировать карточку с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_archive_incorrect_id_card_by_user_causes_error(self, wrong_id, status_code, error_message, user_token):
        response = requests.post(URL.CARDS + wrong_id + "/archive/", headers={'Authorization': f'Bearer {user_token}'})
        assert (response.status_code == status_code and error_message in str(response.json()))
