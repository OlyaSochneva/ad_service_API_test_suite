import allure
import pytest
import requests

from assistant_methods import return_card_status, generate_random_string
from data import URL, Message


def test_create_basic_card(basic_card):
    print(basic_card)


CARD_ID = "895"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMDIwOTQxOCwiaWF0IjoxNzMwMTIzMDE4LCJqdGkiOiIxZjBhOGQ2ZjUzYWI0MGQ4YWIxM2QzODg4N2U3YjJhMiIsImlkIjoxODh9.mR6Z273HmvDkT7o48UT4wZSF3jt1PI74o4fjU5NRh7A"


#                              !!!CHECK CARD STATUS BEFORE RUN!!!
#                                  !!!CARD SHOULD BE ACTIVE!!!

class TestArchiveCardByUser:
    @allure.title('Пользователь может перевести свою карточку в архив')
    @pytest.mark.order(1)
    def test_archive_card_by_user_success(self):
        response = requests.post(URL.CARDS + CARD_ID + "/archive/", headers={'Authorization': f'Bearer {TOKEN}'})
        print(response.json())
        status = return_card_status(response.json())
        assert response.status_code == 200 and status == "archive"

    @allure.title('(404)Пользователь не может архивировать свою карточку, если она уже в архиве')
    @pytest.mark.order(2)
    def test_archive_card_twice_by_user_causes_error(self):
        response = requests.post(URL.CARDS + CARD_ID + "/archive/", headers={'Authorization': f'Bearer {TOKEN}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ACTIVE in str(response.json()))

    # @allure.title('Пользователь не может перевести рандомную чужую карточку в архив')  # доделать!
    # @pytest.mark.order(3)
    # def test_archive_someone_else_card_by_user_causes_error(self):
    #   response = requests.post(URL.CARDS + CARD_ID + "/status/", headers={'Authorization': f'Bearer {TOKEN}'})
    #  status = return_card_status(response.json())
    # assert response.status_code == 200 and status == "status"

    @allure.title('(401)Нельзя архивировать карточку с отсут./невалидным токеном')
    @pytest.mark.order(3)
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_archive_card_unauthorized_causes_error(self, wrong_headers, error_message):
        response = requests.post(URL.CARDS + CARD_ID + "/archive/", headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(404/400)Пользователь не может архивировать карточку с несуществующим/невалидным id')
    @pytest.mark.order(4)
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_archive_incorrect_id_card_by_user_causes_error(self, wrong_id, status_code, error_message):
        response = requests.post(URL.CARDS + wrong_id + "/archive/", headers={'Authorization': f'Bearer {TOKEN}'})
        assert (response.status_code == status_code and error_message in str(response.json()))


#                                !!!CHECK CARD STATUS BEFORE RUN!!!
#                                   !!!CARD SHOULD BE ACTIVE!!!
class TestArchiveCardByAdmin:
    @allure.title('Админ может перевести карточку в архив')
    @pytest.mark.order(1)
    def test_archive_card_by_admin_success(self, admin_token):
        response = requests.post(URL.CARDS + CARD_ID + "/archive/", headers={'Authorization': f'Bearer {admin_token}'})
        status = return_card_status(response.json())
        assert response.status_code == 200 and status == "archive"

    @allure.title('(404)Админ не может архивировать карточку, если она уже в архиве')
    @pytest.mark.order(2)
    def test_archive_card_twice_by_admin_causes_error(self, admin_token):
        response = requests.post(URL.CARDS + CARD_ID + "/archive/", headers={'Authorization': f'Bearer {admin_token}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ACTIVE in str(response.json()))

    @allure.title('(404/400)Админ не может архивировать карточку с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_archive_incorrect_id_card_by_admin_causes_error(self, admin_token, wrong_id, status_code, error_message):
        response = requests.post(URL.CARDS + wrong_id + "/archive/", headers={'Authorization': f'Bearer {admin_token}'})
        assert (response.status_code == status_code and error_message in str(response.json()))
