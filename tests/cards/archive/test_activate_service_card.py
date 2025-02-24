import allure
import pytest
import requests

from assistant_methods import return_card_status, generate_random_string
from data import Message
from admin_data import URL


class TestActivateServiceCard:
    @allure.title('Пользователь может активировать свою карточку услуг')
    def test_activate_service_card_success(self, archive_service):
        response = requests.post(URL.SERVICE_CARDS + archive_service["id"] + "/active/",
                                 headers={'Authorization': f'Bearer {archive_service["token"]}'})
        status = return_card_status(response.json())
        assert (response.status_code == 200 and status == "active")

    @allure.title('(404)Пользователь не может активировать свою карточку услуг, если она уже активна')
    def test_activate_service_card_twice_causes_error(self, active_service):
        response = requests.post(URL.SERVICE_CARDS + active_service["id"] + "/active/",
                                 headers={'Authorization': f'Bearer {active_service["token"]}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ARCHIVE in str(response.json()))

    @allure.title('(404)Пользователь не может активировать карточку услуг на модерации')
    def test_activate_service_card_on_moderation_causes_error(self, new_service):
        response = requests.post(URL.SERVICE_CARDS + new_service["id"] + "/active/",
                                 headers={'Authorization': f'Bearer {new_service["token"]}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ARCHIVE in str(response.json()))

    @allure.title('Пользователь не может активировать чужую архивную карточку услуг')
    def test_activate_another_user_service_card_causes_error(self, user_token, archive_service):
        response = requests.post(URL.SERVICE_CARDS + archive_service["id"] + "/active/",
                                 headers={'Authorization': f'Bearer {user_token}'})
        assert (response.status_code == 403 and Message.NOT_SUFFICIENT_RIGHTS in str(response.json()))

    @allure.title('(401)Нельзя активировать карточку услуг с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_activate_service_card_unauthorized_causes_error(self, wrong_headers, error_message, archive_service):
        response = requests.post(URL.SERVICE_CARDS + archive_service["id"] + "/active/", headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(404/400)Пользователь не может активировать карточку услуг с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_SERVICE_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_activate_service_card_with_incorrect_id_causes_error(self, wrong_id, status_code,
                                                                  error_message, archive_service):
        response = requests.post(URL.SERVICE_CARDS + wrong_id + "/active/",
                                 headers={'Authorization': f'Bearer {archive_service["token"]}'})
        assert (response.status_code == status_code and error_message in str(response.json()))
