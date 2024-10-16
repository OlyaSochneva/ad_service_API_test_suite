import allure
import pytest
import requests

from assistant_methods import return_card_status, generate_random_string
from data import URL, Message


def test_create_card_and_update_status_manually(basic_card):
    print(basic_card)


CARD_ID = "82"

TOKEN = ""


class TestChangeStatusByUser:
    @pytest.mark.order(1)
    def test_move_active_card_to_archive_by_user_success(self):
        response = requests.post(URL.CARDS + CARD_ID + "/archive/",
                                 headers={'Authorization': f'Bearer {TOKEN}'})
        status = return_card_status(response.json())
        assert response.status_code == 200 and status == "archive"

    @pytest.mark.order(2)
    def test_move_card_to_archive_twice_by_user_causes_error(self):
        response = requests.post(URL.CARDS + CARD_ID + "/archive/",
                                 headers={'Authorization': f'Bearer {TOKEN}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ACTIVE in str(response.json()))

    @pytest.mark.order(3)
    def test_move_archive_card_to_active_by_user_success(self):
        response = requests.post(URL.CARDS + CARD_ID + "/active/",
                                 headers={'Authorization': f'Bearer {TOKEN}'})
        status = return_card_status(response.json())
        assert (response.status_code == 200 and status == "active")

    @pytest.mark.order(4)
    def test_move_card_to_active_twice_by_user_causes_error(self):
        response = requests.post(URL.CARDS + CARD_ID + "/active/",
                                 headers={'Authorization': f'Bearer {TOKEN}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ARCHIVE in str(response.json()))

    @allure.title('Err.401 если не передать токен или передать невалидный')
    @pytest.mark.order(5)
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_move_card_to_archive_unauthorized_causes_401_error(self, wrong_headers, error_message):
        response = requests.post(URL.CARDS + CARD_ID + "/archive/", headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('Err.401 если не передать токен или передать невалидный')
    @pytest.mark.order(6)
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_move_card_to_active_unauthorized_causes_401_error(self, wrong_headers, error_message):
        requests.post(URL.CARDS + CARD_ID + "/archive/", headers={'Authorization': f'Bearer {TOKEN}'})
        response = requests.post(URL.CARDS + CARD_ID + "/active/", headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('Err.404/400, если передать неверный id карточки (несуществующий и невалидный - буквы и тд)')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_move_card_to_active_by_incorrect_id_causes_error(self, wrong_id, status_code, error_message):
        response = requests.post(URL.CARDS + wrong_id + "/active/",
                                 headers={'Authorization': f'Bearer {TOKEN}'})
        assert (response.status_code == status_code and error_message in str(response.json()))
        
    @allure.title('Err.404/400, если передать неверный id карточки (несуществующий и невалидный - буквы и тд)')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_move_card_to_archive_by_incorrect_id_causes_error(self, admin_token, wrong_id, status_code, error_message):
        response = requests.post(URL.CARDS + wrong_id + "/archive/",
                                 headers={'Authorization': f'Bearer {admin_token}'})
        assert (response.status_code == status_code and error_message in str(response.json()))


