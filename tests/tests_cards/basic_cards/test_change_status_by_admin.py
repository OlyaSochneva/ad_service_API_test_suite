import allure
import pytest
import requests

from assistant_methods import return_card_status
from data import URL, Message


def test_create_card_and_update_status_manually(basic_card):
    print(basic_card)


CARD_ID = "82"


class TestChangeStatusByAdmin:   # CHECK CARD STATUS BEFORE RUN!!!
    @pytest.mark.order(1)
    def test_move_active_card_to_archive_by_admin_success(self, admin_token):
        response = requests.post(URL.CARDS + CARD_ID + "/archive/",
                                 headers={'Authorization': f'Bearer {admin_token}'})
        status = return_card_status(response.json())
        assert response.status_code == 200 and status == "archive"

    @pytest.mark.order(2)
    def test_move_card_to_archive_twice_by_admin_causes_error(self, admin_token):
        response = requests.post(URL.CARDS + CARD_ID + "/archive/",
                                 headers={'Authorization': f'Bearer {admin_token}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ACTIVE in str(response.json()))

    @pytest.mark.order(3)
    def test_move_archive_card_to_active_by_admin_success(self, admin_token):
        response = requests.post(URL.CARDS + CARD_ID + "/active/",
                                 headers={'Authorization': f'Bearer {admin_token}'})
        status = return_card_status(response.json())
        assert (response.status_code == 200 and status == "active")

    @pytest.mark.order(4)
    def test_move_card_to_active_twice_by_admin_causes_error(self, admin_token):
        response = requests.post(URL.CARDS + CARD_ID + "/active/",
                                 headers={'Authorization': f'Bearer {admin_token}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ARCHIVE in str(response.json()))

    @allure.title('Err.404/400, если передать неверный id карточки (несуществующий и невалидный - буквы и тд)')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_move_card_to_archive_by_incorrect_id_causes_error(self, admin_token, wrong_id, status_code, error_message):
        response = requests.post(URL.CARDS + wrong_id + "/archive/",
                                 headers={'Authorization': f'Bearer {admin_token}'})
        assert (response.status_code == status_code and error_message in str(response.json()))

    @allure.title('Err.404/400, если передать неверный id карточки (несуществующий и невалидный - буквы и тд)')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_move_card_to_active_by_incorrect_id_causes_error(self, admin_token, wrong_id, status_code, error_message):
        requests.post(URL.CARDS + CARD_ID + "/archive/", headers={'Authorization': f'Bearer {admin_token}'})
        response = requests.post(URL.CARDS + wrong_id + "/active/",
                                 headers={'Authorization': f'Bearer {admin_token}'})
        assert (response.status_code == status_code and error_message in str(response.json()))








